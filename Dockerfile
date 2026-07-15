FROM python:3.12-slim

# Install system libraries required by MediaPipe and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgles2 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 config.wsgi:application
