FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app

# Runs to completion: the survey is started with `python scripts/survey_test_photos.py`.
CMD ["python", "scripts/survey_test_photos.py"]
