# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for psycopg2/pillow
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev libjpeg-dev zlib1g-dev \
    libcairo2-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --system


# 3. NOW copy the rest of your project code
COPY . /app/

# Set the settings INSIDE the Railway image
ENV DJANGO_SETTINGS_MODULE=camaramz.settings.prod

# 4. Create the folder and collect files 
RUN mkdir -p /app/staticfiles

# We provide a build-time placeholder for SECRET_KEY so collectstatic doesn't fail.
# Railway will override this with your actual Dashboard variable at runtime.
RUN SECRET_KEY=build-placeholder-123 python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start command
CMD python manage.py migrate_schemas --shared && gunicorn --bind 0.0.0.0:8000 camaramz.wsgi:application