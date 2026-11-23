FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

# Carga los datos de prueba (no duplica si ya existen) y levanta la app con gunicorn
CMD ["sh", "-c", "python seeds.py && gunicorn --bind 0.0.0.0:5000 --workers 2 run:app"]
