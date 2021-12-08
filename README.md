# myblog
Weblog API backend with Django and DRF
# Installation
1 - Clone project

2 - Install pipenv with this command `py -m pip install pipenv` 

3 - Create virtual environment and install packages using `py -m pipenv install` in cloned directory

4 - Create `myblog` table in your mysql database

5 - Create `.env` file in cloned directory and copy & replace `.env.example` with right data into it.

6 - Run `py -m pipenv shell` to activate virtual environment

7 - Migrate database with `py manage.py migrate` command

8 - Create superuser using `py manage.py createsuperuser` command

9 - Start server with `py manage.py runserver` command

10- open http://127.0.0.1:8000/api/v1/docs/ in your browser
