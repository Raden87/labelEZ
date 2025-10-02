# LabelEZ Docker Setup

This document provides instructions for running LabelEZ using Docker with pen input support and zoom controls.

## Features

- **Pen Input Support**: Windows pen devices supported via Pointer Events API
- **Zoom Controls**: Dedicated zoom buttons and keyboard shortcuts
- **Multi-Platform**: Mouse, touch, and stylus input support
- **Health Checks**: Automatic container monitoring
- **Security**: Non-root user and volume isolation

## Prerequisites

- Docker
- Docker Compose (optional, but recommended)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd labelEZ
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d --build
```

Or use the deployment script:
```bash
./deploy.sh
```

3. Access the application:
   - Open your browser and go to `http://localhost:5000`
   - Try zoom controls: `-`, `=`, `R` keys or zoom buttons
   - Pen devices on Windows should work automatically

## Manual Docker Build

If you prefer to build and run manually:

1. Build the Docker image:
```bash
docker build -t labelez .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 \
  -v $(pwd)/images:/app/images \
  -v $(pwd)/labels:/app/labels \
  -v $(pwd)/classes.txt:/app/classes.txt \
  --name labelez-app \
  labelez
```

## Using Docker Hub Image

You can also pull and run the pre-built image from Docker Hub:

```bash
# For local access only
docker run -p 5000:5000 \
  -v $(pwd)/images:/app/images \
  -v $(pwd)/labels:/app/labels \
  -v $(pwd)/classes.txt:/app/classes.txt \
  rantyawset/labelez:latest

# For remote access (bind to all interfaces)
docker run -p 0.0.0.0:5000:5000 \
  -v $(pwd)/images:/app/images \
  -v $(pwd)/labels:/app/labels \
  -v $(pwd)/classes.txt:/app/classes.txt \
  rantyawset/labelez:latest
```

## Remote Deployment

For deploying on a remote server:

1. **Pull the image**:
```bash
docker pull rantyawset/labelez:latest
```

2. **Create directories**:
```bash
mkdir -p images labels
```

3. **Create classes.txt**:
```bash
echo -e "class1\nclass2\nclass3" > classes.txt
```

4. **Run with docker-compose**:
```bash
docker-compose up -d
```

5. **Access remotely**:
   - Open browser and go to `http://<server-ip>:5000`
   - Make sure firewall allows port 5000

## Keyboard Shortcuts

### Navigation
- `B` - Previous image
- `N` - Next image  
- Arrow keys - Previous/Next image

### Zoom & Pan
- `-` - Zoom out
- `=` - Zoom in
- `R` - Reset zoom and pan
- `Space + Drag` - Pan view
- `Mouse wheel` - Zoom

### Drawing
- `S` - Save annotations
- `Z` - Undo last point
- `X` - Delete current polygon
- Click to add points
- Click initial point to close polygon

### Class Selection
- `1-9` - Select classes 0-8
- `0` - Select class 9
- `Q-P` - Select classes 10-19

## Volume Mounts

The Docker setup mounts the following directories:
- `./images` → `/app/images` - For storing images to label
- `./labels` → `/app/labels` - For storing label files
- `./classes.txt` → `/app/classes.txt` - For class definitions

## Environment Variables

- `FLASK_ENV=development` - Sets Flask to development mode
- `FLASK_DEBUG=1` - Enables Flask debug mode

## Stopping the Application

To stop the application:
```bash
docker-compose down
```

## Development

For development, you can mount the source code as a volume:

```bash
docker run -p 5000:5000 \
  -v $(pwd):/app \
  -v $(pwd)/images:/app/images \
  -v $(pwd)/labels:/app/labels \
  rantyawset/labelez:latest
```

This will allow you to make changes to the code without rebuilding the image.

## Troubleshooting

1. **Port already in use**: Make sure port 5000 is not being used by another application
2. **Permission issues**: Ensure the Docker daemon has access to the mounted directories
3. **Build failures**: Check that all dependencies are properly listed in `requirements.txt`
