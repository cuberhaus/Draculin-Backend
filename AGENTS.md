# Draculin-Backend

BitsXLaMarató 2023 hackathon finalist. Django REST API for the Draculin sexual and reproductive health app — news, chatbot, quiz, computer-vision analysis, and stats endpoints. Paired with [Draculin-Front](../Draculin-Front) (Flutter web).

## Architecture

- **Stack:** Django 5.0 + django-rest-framework, Python 3.11, SQLite (`db.sqlite3`), Docker.
- **Project:** [Draculin/](Draculin/) (settings, urls, wsgi/asgi, Sentry obs).
- **App:** [dracu/](dracu/) (models, views, serializers, `inference_image.py` for vision).
- **External:** Google Bard (`bard_api.py`, `bard.sh`), Roboflow (vision); both run in mock mode if keys are missing.

## Build and Test

```bash
docker compose up -d        # backend :8889, frontend :8890
docker compose down
python manage.py test       # Django tests (dracu/tests.py)
```

Local (no Docker): `pip install -r requirements.txt && python manage.py migrate && python manage.py runserver`.

## Pitfalls

- Hackathon code, treat as frozen — avoid refactors.
- Fork of `BITS2023/Draculin-Backend`; upstream is archived.
- `requirements.txt` is UTF-16 encoded; Docker uses `requirements-docker.txt` instead.
- Audit for hardcoded API keys (Bard, Roboflow) before any public push and rotate if found.
- `db.sqlite3` is committed with seed data — do not wipe.

See [README.md](README.md).
