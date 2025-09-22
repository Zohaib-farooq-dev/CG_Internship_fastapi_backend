# ---- 1. Base Image ----
FROM python:3.11-slim

# ---- 2. Set working directory ----
WORKDIR /app

# ---- 3. Copy requirements first (for caching) ----
COPY requirements.txt .

# ---- 4. Install Python dependencies ----
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ---- 4. Copy the project code ----
COPY . .

# ---- 6. Expose port ----
EXPOSE 8000

# ---- 7. Run FastAPI with Uvicorn ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
