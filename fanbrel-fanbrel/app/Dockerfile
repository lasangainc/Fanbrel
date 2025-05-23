FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    python3-rpi.gpio \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p /data

# Make scripts executable
RUN chmod +x fan_control.py

# Expose port for web UI
EXPOSE 3500

# Run the fan control script
CMD ["python3", "fan_control.py"] 