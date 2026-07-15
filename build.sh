#!/usr/bin/env bash
set -e

echo '==> Installing system libraries for MediaPipe/OpenCV...'
apt-get install -y --no-install-recommends libgles2 libgl1 libglib2.0-0 libsm6 libxrender1 libxext6

echo '==> Installing Python dependencies...'
pip install -r requirements.txt

echo '==> Collecting static files...'
python manage.py collectstatic --noinput
