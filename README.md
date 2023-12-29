# FULLSTACK HEALTH & FITNESS

Commercial freelance project.

## Description

Web service for managing clients by fitness specialists.

Main features:
- Tracking physical indicators and anthropometry.
- Management of exercises and workouts.
- Monitoring nutrition and calculating macronutrients (integration with the fatsecret app).
- Chat system between fitness expert and clients.

## Demo

https://www.fullstack-fitness.com/

## Technologies

Django, SQLite, HTML, CSS, Javascript, Jquery, Bootstrap.

## Installation

- create .env file with your settings according to .env.example

- create virtual environment and activate it
```
python -m venv venv
venv\Scripts\activate
```

- install requirements
```
pip install -r requirements.txt
```

- run migrations, load fixtures and collect static files
```
python manage.py migrate
python manage.py loaddata ./fixtures/metrics_colors.json
python manage.py loaddata ./fixtures/training_areas.json
python manage.py loaddata ./fixtures/training_tools.json
python manage.py collectstatic
```

- create superuser-expert because it is mandatory
```
python manage.py createexpert
```

- run server
```
python manage.py runserver
```