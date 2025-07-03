FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the index_api directory and data
COPY index_api/ ./index_api/
COPY data/company_financial_indexes.csv ./data/

# Set the working directory to index_api
WORKDIR /app/index_api

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 