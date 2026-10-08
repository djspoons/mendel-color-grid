FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Runs to completion: writes docs/picture-method-results.md and previews.
CMD ["python", "-m", "picture_method"]
