FROM python:3.12-slim
WORKDIR /app
COPY . /app
# Runs to completion; no server. Run the survey with:
#   python scripts/survey_test_photos.py
CMD ["python", "scripts/survey_test_photos.py"]
