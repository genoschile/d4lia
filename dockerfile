FROM python:3.11-slim

# Crea directorio de la app
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . .

CMD ["celery", "-A", "app.worker", "worker", "--loglevel=INFO"]
