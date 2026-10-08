FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Runs to completion and writes docs/picture-method-results.md; nothing listens on a port.
CMD ["python", "run_picture_method.py"]
