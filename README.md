# LabelEZ - YOLO Polygon Labeling Tool

A web-based polygon labeling tool for creating YOLO format annotations with an intuitive interface.

## Features

- **Polygon Drawing**: Click to add points, click first point to close polygon
- **Class Selection**: 6 predefined classes with color-coded buttons
- **Zoom & Pan**: Mouse wheel to zoom, Space+move to pan
- **Keyboard Shortcuts**: 
  - `S` - Save
  - `Z` - Undo last point
  - `X` - Delete current polygon
  - `B` - Back to previous image
  - `N` - Next image
  - `1-6` - Select class
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
6. Update `classes.txt` with your class names (one per line)
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

1. **Select Class**: Click class buttons or use number keys 1-6
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
