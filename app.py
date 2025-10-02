# app.py
from flask import Flask, send_from_directory, request, jsonify, render_template
import os, json

app = Flask(__name__, template_folder="templates", static_folder="static")

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
    data = request.json
    img_name = data["image"]
    anns = data["annotations"]
    out_file = os.path.join(LABELS_DIR, os.path.splitext(img_name)[0] + ".txt")

    with open(out_file, "w") as f:
        for ann in anns:
            cid = ann["class_id"]
            pts = " ".join(f"{x:.6f} {y:.6f}" for x, y in ann["points"])
            f.write(f"{cid} {pts}\n")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    os.makedirs(LABELS_DIR, exist_ok=True)
    app.run(debug=True)
