# Installation Manual

## Basic Setup

Before you start you need to make sure, that Python 3.6.5 is installed on your system. Also all of our files including the database must be extracted from the zip folder. 

To install all necessary Python dependencies run the following from the command prompt.

macOS: ``pip3 install -r requirements.txt``

windows: ``pip install -r requirements.txt``

## Starting the server

After we installed our Python packages including the main framework 'Django',we are ready to start the server. 

To start the server on localhost run these commands in your command prompt.

macOS: ``python3 manage.py runserver``

windows: `` python manage.py runserver``

Now you should open your browser at ``127.0.0.1:8000`` to view the web page. 