# Copilot Instructions for shopsite-backend

## Overview
This is a Django-based backend for an e-commerce platform. The project is organized by Django apps, each responsible for a domain area (e.g., `shop`, `cart`, `lists`, `qna`, `review`, `users`). The main configuration is under `config/`.

## Architecture & Key Components
- **Django Apps**: Each folder at the top level (e.g., `shop/`, `cart/`, `lists/`, `qna/`, `review/`, `users/`) is a Django app with its own models, views, urls, and templates.
- **Settings**: All global settings are in `config/settings.py`.
- **Database**: Uses `db.sqlite3` by default. Migrations are managed per app in their `migrations/` subfolders.
- **Static & Media**: Static files are under each app's `static/` directory. Media uploads are in `mediafiles/`.
- **Templates**: App-specific templates are in `templates/<app>/` within each app.

## Developer Workflows
- **Run server**: `python manage.py runserver`
- **Migrate DB**: `python manage.py makemigrations && python manage.py migrate`
- **Create superuser**: `python manage.py createsuperuser`
- **Run tests**: `python manage.py test <app>`
- **Import products**: `python import_products.py` (custom script)

## Project Conventions
- **App Structure**: Each app follows Django conventions: `models.py`, `views.py`, `urls.py`, `admin.py`, `forms.py` (if needed), and `templates/<app>/`.
- **URL Routing**: All app URLs are included in `config/urls.py`.
- **Custom Scripts**: Place one-off scripts (e.g., data import) at the project root.
- **Media Organization**: Product/review images are organized under `mediafiles/shop/` and `mediafiles/review/`.

## Integration & Dependencies
- **requirements.txt**: All Python dependencies are listed here. Install with `pip install -r requirements.txt`.
- **No non-Django services**: All logic is handled within Django; no microservices or external APIs are directly integrated.

## Examples
- To add a new model, create it in the relevant app's `models.py`, run migrations, and register it in `admin.py`.
- To add a new page, create a view in `views.py`, a template in `templates/<app>/`, and map the URL in `urls.py`.

## Key Files & Directories
- `config/settings.py`: Global Django settings
- `shop/models.py`, `cart/models.py`, etc.: Domain models
- `mediafiles/`: Uploaded images
- `requirements.txt`: Python dependencies

---
For questions about project-specific patterns, check the structure of existing apps for examples.
