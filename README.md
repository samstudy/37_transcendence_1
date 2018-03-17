# Transcendence project

This project is a first iteration of Transcendence project,according it was done below tasks:

- Create project
- Add view for look information about user(by link:/users/1)
- Login to [Sentry](https://sentry.io/) and setup LOGGING
- Setup [django-configurations](https://github.com/jazzband/django-configurations) for convenient configuration
- Create fab script which will be deploy the project on remote production server


## How to Use

Step 1. Install modules from requirement 

Step 2. Insert sample information(python manage.py shell)

Step 3. Launch the server 

Example of  launch on Linux, Python 3.5:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py shell
(InteractiveConsole)
>>>
from django.contrib.auth.models import User

user = User(username='Ivan', first_name = 'Ivan',last_name='Ivanov', 
date_joined = '2002-01-01',email = 'ivan@gmail.com',)
user.save()
exit()
python manage.py runserver

```
## How to install on remote production server.In this case a server will available by this link[http://159.89.116.66](http://159.89.116.66).

Step 1. Create SSH folder manually:

```
mkdir ~/.ssh
chmod 0700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 0644 ~/.ssh/authorized_keys

```

Step 2. Paste the SSH public key into your ~/.ssh/authorized_keys file(Take public key from remote server)

```
sudo vim ~/.ssh/authorized_keys

```
Step 3. Deploy the fab file

```
fab fab_bootstrap:host=root@159.89.116.66

```
The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

