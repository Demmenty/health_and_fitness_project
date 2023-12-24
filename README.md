# HEALTH & FITNESS

Commercial freelance project.

## Description

Web service for managing clients by fitness specialists.

Main features:
- Tracking physical indicators and anthropometry.
- Management of exercises and workouts.
- Monitoring nutrition and calculating macronutrients (integration with the fatsecret app).
- Chat system between fitness expert and clients.

## Demo

https://healthfitness-demmenty.pythonanywhere.com

## Technologies

Django, SQLite, HTML, CSS, Javascript, Jquery, Bootstrap.

## Installation

create .env file with your settings according to .env.example

```
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata ./fixtures/metrics_colors.json
python manage.py loaddata ./fixtures/training_areas.json
python manage.py loaddata ./fixtures/training_tools.json
python manage.py collectstatic
python manage.py createexpert
python manage.py runserver
```