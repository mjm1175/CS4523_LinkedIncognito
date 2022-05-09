DATABASE INSTRUCTIONS AND INFO

host name: ubuntu-s-1vcpu-1gb-nyc1-01
password: g$?QaedtDe92uJE
IP address: 159.203.182.153

users: (to switch: `su aj`)
maria
ziggy

aj
ziggy

tehya
ziggy


Postgres:
database: LinkedIncognito
user: LIuser
password: ziggy

Virtualenv: LIenv

django project: LIapp


Superuser:
username: maria
email: mjm1175@nyu.edu
password: ziggy

username: aj
email: ajo331@nyu.edu
password: ziggy

username: tehya
email: tt1748@nyu.edu
password: ziggy

{% load static %} at top of html files

Run server: python manage.py runserver 0.0.0.0:8000

Start Up:
	>ssh root@159.203.182.153
		password:g$?QaedtDe92uJE
	$ su maria
		password:ziggy
	$ cd
	$ cd dev/LinkedIncognito/LinkedIncognito
	$ source LIenv/bin/activate
	$ cd LIapp

that port is already in use error: sudo fuser -k 8000/tcp

create new app:
	python manage.py startapp <appname>
	add to INSTALLED_APPS in LIapp/settings.py

after any edits to models.py:
	python manage.py makemigrations
	python manage.py migrate

if you want a class (model) attribute to be optional:
	in models.py set null=True, blank=True
	in forms.py set required=False