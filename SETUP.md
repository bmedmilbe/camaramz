# 📋 Setup & Installation Guide

This project utilizes **Pipenv** for dependency management and **Docker** for orchestration. Environment-specific configurations are handled via the `DJANGO_SETTINGS_MODULE` variable.

---

## 🛠️ Prerequisites

- **Python 3.10+**
- **Pipenv** (`pip install pipenv`)
- **Docker & Docker Compose**
- **PostgreSQL**

---

## 🚀 Local Development Setup

### 1. Environment Activation

```bash
pipenv install --dev
pipenv shell


2. Configuration (Environment Variables)
The system is pre-configured to use production settings in Docker. For local development, you must point to the dev module in your terminal:
On Windows (PowerShell):

PowerShell


$env:DJANGO_SETTINGS_MODULE="camaramz.settings.dev"


On macOS/Linux:

Bash


export DJANGO_SETTINGS_MODULE=camaramz.settings.dev


3. Database Initialization

Bash


python manage.py migrate
python manage.py createsuperuser


🐳 Docker Deployment (Production)
The Dockerfile and docker-compose.yml are optimized for production. They contain the following default configuration:
ENV DJANGO_SETTINGS_MODULE=camaramz.settings.prod
Running with Docker Compose:

Bash


docker-compose up --build


This will automatically:
Build the Django application.
Spin up a PostgreSQL database.
Configure Gunicorn to serve the app using Production settings.
✅ Verification Checklist
[ ] Pipenv environment active.
[ ] DJANGO_SETTINGS_MODULE correctly set for the current environment.
[ ] Admin panel accessible at /admin/.
[ ] Swagger API docs accessible at /api/swagger/.
Maintained by: Edmilbe Ramos
```
