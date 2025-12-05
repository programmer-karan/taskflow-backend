# 1. Base Image: Use a lightweight Python Linux image
FROM python:3.11-slim

# 2. Setup Environment Variables
# - Convert stdout/stderr to unbuffered (logs show up immediately)
# - Don't create .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Set Working Directory
WORKDIR /app

# 4. Install Dependencies (Cached Layer)
# We copy requirements first so Docker caches the installation step
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy Source Code
COPY . .

# 6. Expose the port
EXPOSE 8000

# 7. Command to run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]