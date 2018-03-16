import os
from fabric.contrib.files import append, exists
from fabric.context_managers import settings
from fabric.api import cd, env, run, sudo


DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PSWD = os.environ['DB_PSWD']
REPO_URL = 'https://github.com/samstudy/37_transcendence_1.git'
SPLIT_GIT = 0
SPLIT_PRJ_NAME = 4
DIRECTORIES = {
    'PRJ_DIR': '/opt/web_apps',
    'VENV_DIR': '/opt/my_env'
    }
PRJ_FOLDER = os.path.join(DIRECTORIES['PRJ_DIR'], REPO_URL.split('.git')
                          [SPLIT_GIT].split('/')[SPLIT_PRJ_NAME])
VIRTENV = os.path.join(DIRECTORIES['VENV_DIR'], REPO_URL.split('.git')
                       [SPLIT_GIT].split('/')[SPLIT_PRJ_NAME])


def prepare_packages():
    run("sudo apt-get update")
    run("sudo apt-get upgrade")
    run("sudo sudo apt-get install build-essential "
        "libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip")
    run("sudo apt-get install python3-pip python3-dev "
        "libpq-dev postgresql postgresql-contrib nginx")
    run("sudo pip3 install --upgrade pip")
    run("sudo apt-get install python-virtualenv")
    run("sudo apt-get install git")
    sudo("apt-get install uwsgi")


def run_as_pg_user(command):
    return sudo('sudo -i -u postgres %s' % command)


def is_pg_user_exists(username):
    with settings(warn_only=True):
        res = run_as_pg_user('''psql -t -A -c "SELECT COUNT(*) /
              FROM pg_user WHERE usename = '%(username)s';"''' % locals())
    return res == 1


def is_pg_database_exists(database):
    with settings(warn_only=True):
        res = run_as_pg_user('''psql -t -A -c "SELECT COUNT(*) /
              FROM pg_database WHERE datname = '%(database)s';"''' % locals())
    return res == 1


def grant_privileges_on_db(database, username):
    run_as_pg_user('''psql -t -A -c "GRANT ALL PRIVILEGES ON DATABASE /
                  %(database)s TO %(username)s;"''' % locals())


def pg_create_user(username, password):
    run_as_pg_user('''psql -t -A -c "CREATE USER %(username)s /
                   WITH PASSWORD '%(password)s';"''' % locals())


def pg_create_database(database, owner):
    run_as_pg_user('createdb %(database)s -O %(owner)s' % locals())


def create_folders():
    for folder in DIRECTORIES.values():
        with settings(warn_only=True):
            if not exists(os.path.abspath(folder)):
                run("mkdir %s" % (os.path.abspath(folder)))


def get_latest_source_code():
    with settings(warn_only=True):
        if exists(os.path.abspath(PRJ_FOLDER)):
            with cd(os.path.abspath(PRJ_FOLDER)):
                run('git fetch origin')
                run('git reset --hard origin/master')
        else:
            with cd(os.path.abspath(DIRECTORIES['PRJ_DIR'])):
                run('git clone %s' % (REPO_URL))


def create_virt_and_install_req():
    run('sudo virtualenv %s' % (os.path.abspath(VIRTENV)))
    with cd(os.path.abspath(PRJ_FOLDER)):
            run('source %s/bin/activate && \
                pip install -r requirements.txt' % (os.path.abspath(VIRTENV)))


def setup_ngnix():
    run('sudo ln -s ~/opt/webapp/37_transcendence_1/nginx_conf '
        '/etc/nginx/sites-enabled/')
    run('sudo /etc/init.d/nginx restart')


def fab_bootstrap():
    prepare_packages()
    if not is_pg_user_exists(DB_USER):
        pg_create_user(DB_USER, DB_PSWD)
    if not is_pg_database_exists(DB_NAME):
        pg_create_database(DB_NAME, DB_USER)
    grant_privileges_on_db(DB_NAME, DB_USER)
    create_folders()
    get_latest_source_code()
    create_virt_and_install_req()
    setup_ngnix()
