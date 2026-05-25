FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev libjpeg-dev zlib1g-dev \
    libcairo2-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

# 1. Copy the Pipfiles from your specific subfolder
COPY cms_project/Pipfile cms_project/Pipfile.lock /app/
RUN pipenv install --deploy --system

# 2. REACH INTO THE CORE FOLDER (This works now because Root Directory is '/')
COPY core /app/core

# 3. Copy everything else inside the cms_project folder into the app root
COPY tour_project/ /app/

ENV DJANGO_SETTINGS_MODULE=camaramz.settings.prod
RUN mkdir -p /app/staticfiles
RUN SECRET_KEY=build-placeholder-123 python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py migrate_schemas && gunicorn --bind 0.0.0.0:8000 camaramz.wsgi:application
