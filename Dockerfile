FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# Runs to completion: surveys the open sources and writes docs/test-photo-set-survey.md.
# Standard library only, so there is nothing to install.
CMD ["python", "docs/team-shot-plan/survey.py"]
