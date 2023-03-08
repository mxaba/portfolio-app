# Portfolio_App

Portfolio App using Django Backend with authentication system.

### GETTING STARTED

1 - Install requirements 
```
pip install -r requirements.txt
```

2 - Install postgresql and pgadmin and create a database inside pgadmin. Then change the database settings inside Settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'portfolio',
        'USER': 'mxaba',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
```

3 - Make Migrations 
```
python manage.py makemigrations
python manage.py migrate
```

4 - Runserver on port 8000
```
python manage.py runserver

http://127.0.0.1:8000/
```

5 - Create superuser 
```
python manage.py createsuperuser
```
