FROM python:3.9-slim

WORKDIR /app

COPY fan_control.py .

CMD ["python", "fan_control.py"]
