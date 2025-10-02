# LabelEZ - YOLO Polygon Labeling Tool

A web-based polygon labeling tool for creating YOLO format annotations with an intuitive interface.

## Features

- **Polygon Drawing**: Click to add points, click first point to close polygon
- **Class Selection**: Configurable classes with color-coded buttons
- **Zoom & Pan**: Mouse wheel to zoom, Space+move to pan
- **Keyboard Shortcuts**: 
  - `S` - Save
  - `Z` - Undo last point
  - `X` - Delete current polygon
  - `B` - Back to previous image
  - `N` - Next image
  - `1-0` - Select class (1-9 for classes 0-8, 0 for class 9)
  - `Q-P` - Select class (Q for class 10, W for class 11, etc. up to P for class 19)
- **Auto-save**: Automatically saves when polygons are completed
- **Label Loading**: Loads existing labels when switching images

## Setup

1. Install Python 3.8+
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install flask
   ```
4. Create required directories:
   ```bash
   mkdir images labels
   ```
5. Add your images to the `images/` directory
6. Update `classes.txt` with your class names (one per line, supports up to 20 classes)
7. Run the application:
   ```bash
   python app.py
   ```
8. Open http://localhost:5000 in your browser

## File Structure

```
labelEZ/
├── app.py              # Flask backend
├── classes.txt         # Class definitions
├── templates/
│   └── index.html      # Frontend interface
├── images/             # Your images (not included in repo)
├── labels/             # Generated label files (not included in repo)
└── venv/               # Virtual environment
```

## Usage

1. **Select Class**: Click class buttons or use keyboard shortcuts (1-0 for first 10 classes, Q-P for classes 10-19)
2. **Draw Polygon**: Click to add points, click first point to close
3. **Edit**: Drag points to adjust, use Z to undo, X to delete
4. **Navigate**: Use B/N keys or buttons to switch images
5. **Save**: Press S or auto-saves when polygon is closed

## Label Format

Labels are saved in YOLO polygon format:
```
class_id x1 y1 x2 y2 x3 y3 ...
```

Where coordinates are normalized (0-1) relative to image dimensions.

## Security Note

The `images/` and `labels/` directories are excluded from version control to protect sensitive data. Add your own images and the tool will generate labels locally.
