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
    return jsonify(files)

@app.route("/image/<path:filename>")
def get_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route("/load/<path:filename>")
def load_labels(filename):
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

if __name__ == "__main__":
    os.makedirs(LABELS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # Get environment variables
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
