#!/bin/bash
# Build script for Swasthya Twin - builds React app then prepares for Python deployment

echo "Building React frontend..."
cd working
npm install
npm run build
cd ..

echo "Copying React build to static folder..."
rm -rf static
cp -r working/dist static

echo "Fixing asset paths for subdirectory serving..."
sed -i 's|"/assets/|"./assets/|g' static/index.html

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build complete!"
