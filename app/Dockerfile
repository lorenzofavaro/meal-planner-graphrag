# Build stage
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Final stage
FROM python:3.11-slim AS runtime

# Set working directory
WORKDIR /app

# Copy the dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the source code
COPY . .

# Expose Chainlit port
EXPOSE 8501

# Start Chainlit
CMD ["chainlit", "run", "--host", "0.0.0.0", "--port", "8501", "app.py"]
