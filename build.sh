#!/bin/bash
# Build script for Render deployment
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements-prod.txt

echo "Running Django checks..."
python manage.py check --deploy

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
