#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install 
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata paises.json
#if [[ $CREATE_SUPERUSER ]];
#then
#python manage.py createsuperuser --no-input
#fi

