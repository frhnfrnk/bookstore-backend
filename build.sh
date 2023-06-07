#!/bin/sh

# Build the project
echo "Building the project..."
python -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect static files..."
python3 manage.py collectstatic --noinput --clear
