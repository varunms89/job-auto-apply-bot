FROM python:3.11-slim

WORKDIR /app

# Ensure unbuffered python output for real-time logs
ENV PYTHONUNBUFFERED=1
ENV SCAN_INTERVAL_SECONDS=3600

# Copy project files
COPY . /app

# Run continuous background bot
CMD ["python", "live_bot.py"]
