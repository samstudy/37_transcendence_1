# Transcendence project

This project is a first iteration of Transcendence project,according it was done below tasks:

- Create project
- Add view for look information about user(by link:/users/1)
- Login to [Sentry](https://sentry.io/) and setup LOGGING
- Setup [django-configurations](https://github.com/jazzband/django-configurations) for convenient configuration



## How to Use

Step 1. Install modules from requirement 

Step 2. Create and apply the database 

Step 3. Insert sample information(python manage.py shell)

Step 4. Launch the server 

Example of  launch on Linux, Python 3.5:

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py shell
(InteractiveConsole)
>>>
from first_iteration.models import UserInformation
user = UserInformation(name='Ivan', last_name='Ivanov', education = 'MIT',city = 'Moscow',
profession = 'developer',birth_day = '2002-01-01',gmail = 'ivan@gmail.com',
facebook = 'facebook.com/ivanov', vk = 'vk.com/ivanov', github = 'github.com/ivanov')
user.save()
exit()
python manage.py runserver

```

#### The sample out from link:/users/1
![37](https://user-images.githubusercontent.com/22424468/36070464-47204e72-0f25-11e8-9fa3-88d2cb18fa07.JPG)

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

