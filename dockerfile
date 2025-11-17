FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy reqs
COPY requirements.txt .

# Install deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Default command overridden by docker-compose
CMD ["python", "app/main.py"]
