#!/bin/bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py validate
python manage.py syncdb
python manage.py runserver &
x-www-browser localhost:8000 &