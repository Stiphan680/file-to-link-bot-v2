FROM python:3.11-slim

# Set environment variable for unbuffered Python output
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port for health check
EXPOSE 8080

# Start the bot with unbuffered output
CMD ["python", "-u", "bot.py"]
