#!/bin/bash

# Start script for labelEZ application

# Create necessary directories
mkdir -p images labels

# Set proper permissions
chmod -R 755 images labels

# Start the application
exec python app.py
