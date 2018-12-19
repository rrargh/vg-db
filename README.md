# Simple database management tool using built-in Django admin interface

## About
This is a simple database management tool for creating, viewing, updating and deleting members, coaches and small groups of a local church organization.

## Tech Stack
* Python
* Django
* PostgreSQL

## Requirements
* Python 2.7
* Django 1.10

## Installation guide
This guide assumes you are using Ubuntu 18.04
Install basic requirements such as Python 2.7, Git and PostgreSQL
```
sudo apt-get install python git postgresql
```

Install Pip and Virtualenv
```
sudo apt-get install pip virtualenv
```


Create virtual environment in desired directory, and activate it
```
virtualenv venv
source venv/bin/activate
```

Make a local copy of the project
```
git clone https://github.com/rrargh/vg-db.git
```

Go to project root and use Pip to install the other dependencies:
```
cd vg-db
pip install -r requirements.txt
```

After updating *settings.py*, initialize database:
```python
python manage.py migrate
```

## Running the app
Run the app by going to the ludare_project/ludare_project folder and typing:
```python
python manage.py runserver
```

On your web browser, access the app admin interface by going to:
http://127.0.0.1:8000/admin/

