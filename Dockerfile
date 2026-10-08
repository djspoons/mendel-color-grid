FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Runs to completion: regenerates photos/, docs/picture-method-results.md and
# docs/picture-method/quantize-vote/. It does not listen on any port.
CMD ["python", "run_picture_method.py"]
