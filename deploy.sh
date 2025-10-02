#!/bin/bash

# Deployment script for labelEZ

echo "🚀 Starting labelEZ deployment..."

# Stop existing containers
echo "📦 Stopping existing containers..."
docker-compose down

# Build and start the application
echo "🔨 Building and starting labelEZ..."
docker-compose up --build -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ labelEZ is running successfully!"
    echo "🌐 Access the application at: http://localhost:5000"
    echo "📊 Container status:"
    docker-compose ps
else
    echo "❌ Application failed to start. Checking logs..."
    docker-compose logs
    exit 1
fi

echo "🎉 Deployment complete!"
