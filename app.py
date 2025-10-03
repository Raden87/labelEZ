# app.py
from flask import Flask, send_from_directory, request, jsonify, render_template
from flask_cors import CORS
import os, json

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app, resources={
    r"/save": {"origins": "*"},
    r"/load/*": {"origins": "*"},
    r"/classes": {"origins": "*"},
    r"/images": {"origins": "*"},
    r"/image/*": {"origins": "*"}
})

IMAGES_DIR = "images"
LABELS_DIR = "labels"
CLASSES_FILE = "classes.txt"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classes")
def get_classes():
    with open(CLASSES_FILE, "r") as f:
        classes = [line.strip() for line in f if line.strip()]
    return jsonify(classes)

@app.route("/images")
def list_images():
    files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpg",".png"))]
    files.sort()  # Sort files to ensure consistent ordering
    return jsonify(files)

@app.route("/image/<path:filename>")
def get_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route("/load/<path:filename>")
def load_labels(filename):
    # Verify that the image file actually exists
    img_file_path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(img_file_path):
        print(f"WARNING: Attempted to load labels for non-existent image: {filename}")
        return jsonify([])
    
    label_file = os.path.join(LABELS_DIR, os.path.splitext(filename)[0] + ".txt")
    
    if not os.path.exists(label_file):
        return jsonify([])
    
    annotations = []
    with open(label_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 7:  # Need at least class_id + 3 points (6 coordinates)
                continue
            
            class_id = int(parts[0])
            points = []
            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    x = float(parts[i])
                    y = float(parts[i + 1])
                    points.append([x, y])
            
            if len(points) >= 3:  # Valid polygon needs at least 3 points
                annotations.append({
                    "class_id": class_id,
                    "points": points
                })
    
    return jsonify(annotations)

@app.route("/save", methods=["POST"])
def save_labels():
    try:
        data = request.json
        if not data:
            response = jsonify({"error": "No data received"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
            
        img_name = data.get("image")
        anns = data.get("annotations", [])
        
        if not img_name:
            response = jsonify({"error": "No image name provided"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
        
        # Verify that the image file actually exists
        img_file_path = os.path.join(IMAGES_DIR, img_name)
        if not os.path.exists(img_file_path):
            print(f"WARNING: Attempted to save labels for non-existent image: {img_name}")
            response = jsonify({"error": f"Image file {img_name} does not exist"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
            
        out_file = os.path.join(LABELS_DIR, os.path.splitext(img_name)[0] + ".txt")

        with open(out_file, "w") as f:
            for ann in anns:
                cid = ann["class_id"]
                pts = " ".join(f"{x:.6f} {y:.6f}" for x, y in ann["points"])
                f.write(f"{cid} {pts}\n")

        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        response = jsonify({"error": str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

@app.route("/label-status/<filename>")
def check_label_status(filename):
    """Check if a label file exists for a given image filename"""
    label_file = os.path.join(LABELS_DIR, os.path.splitext(filename)[0] + ".txt")
    has_label = os.path.exists(label_file)
    
    response = jsonify({"has_label": has_label})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/label-status-all")
def check_all_label_status():
    """Check label status for all images at once"""
    image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpg", ".png"))]
    image_files.sort()
    
    status_map = {}
    total_classes = 6  # Based on classes.txt
    
    for img_file in image_files:
        label_file = os.path.join(LABELS_DIR, os.path.splitext(img_file)[0] + ".txt")
        has_label = os.path.exists(label_file)
        
        if has_label:
            try:
                with open(label_file, "r") as f:
                    lines = f.readlines()
                    valid_polygon_count = 0
                    unique_classes = set()
                    for line in lines:
                        line = line.strip()
                        if line:  # Non-empty line
                            parts = line.split()
                            # Valid polygon format: class_id + at least 6 coordinate values (3 points)
                            if len(parts) >= 7 and len(parts) % 2 == 1:  # Odd number = class + pairs
                                valid_polygon_count += 1
                                class_id = int(parts[0])
                                if 0 <= class_id < total_classes:  # Valid class ID
                                    unique_classes.add(class_id)
                    
                    print(f"{img_file}: {valid_polygon_count} valid polygons, {len(unique_classes)} unique classes (0-{total_classes-1})")
                    
                    if valid_polygon_count == 0:
                        status_map[img_file] = "none"  # Has label file but no valid polygons
                    elif valid_polygon_count >= total_classes and len(unique_classes) < total_classes:
                        status_map[img_file] = "yellow"  # X+ polygons but not all classes present
                    elif len(unique_classes) < total_classes:
                        status_map[img_file] = "orange"  # Missing classes
                    else:
                        status_map[img_file] = "green"  # All classes present - complete coverage
            except:
                status_map[img_file] = "none"  # Error reading file
        else:
            status_map[img_file] = "none"  # No label file
    
    response = jsonify(status_map)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    os.makedirs(LABELS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # Get environment variables
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
