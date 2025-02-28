FROM python:3.10
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

CMD ["python", "indexer.py"]
