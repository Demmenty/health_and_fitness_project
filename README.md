# FULLSTACK FITNESS

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

<details>
  <summary>Screenshots</summary>
  
> ![screen1](https://github.com/Demmenty/health_and_fitness_project/assets/109406056/70f9d4df-24e6-4ff3-a504-8a0598290497)
> 
> ![screen2](https://github.com/Demmenty/health_and_fitness_project/assets/109406056/aa286b56-fd20-445a-a1ca-ac3d63f316a0)
> 
> ![screen3](https://github.com/Demmenty/health_and_fitness_project/assets/109406056/874d27b8-9750-4c3f-a74e-0fcf7089df2d)
> 
> ![screen4](https://github.com/Demmenty/health_and_fitness_project/assets/109406056/2c06aeaa-0e83-432b-852c-1c615d738160)

</details>

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
