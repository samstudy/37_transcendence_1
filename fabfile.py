import os
from fabric.contrib.files import append, exists
from fabric.context_managers import settings
from fabric.api import cd, env, run, sudo


DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PSWD = os.environ['DB_PSWD']
REPO_URL = 'https://github.com/samstudy/37_transcendence_1.git'
USEFUL_INDEX_GIT = 0
USEFUL_INDEX_PRJ_NAME = 4
DIRECTORIES = {
    'PRJ_DIR': '/opt/web_apps',
    'VENV_DIR': '/opt/my_env'
    }
PRJ_FOLDER = os.path.join(DIRECTORIES['PRJ_DIR'], REPO_URL.split('.git')
                          [USEFUL_INDEX_GIT].split('/')[USEFUL_INDEX_PRJ_NAME])
VIRTENV = os.path.join(DIRECTORIES['VENV_DIR'], REPO_URL.split('.git')
                       [USEFUL_INDEX_GIT].split('/')[USEFUL_INDEX_PRJ_NAME])
NGINX_CONF = os.path.join(PRJ_FOLDER, 'nginx_conf/nginx_conf')


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
    run("sudo apt-get install uwsgi")


def is_pg_user_exists(username):
    with settings(warn_only=True):
        res = run('''
            sudo -i -u postgres psql -t -A -c "SELECT COUNT(*)
            FROM pg_user WHERE usename = '%s'"''' % username)
    return res == '1'


def is_pg_database_exists(database):
    with settings(warn_only=True):
        res = run('''
            sudo -i -u postgres psql -t -A -c "SELECT COUNT(*)
            FROM pg_database WHERE datname='%s'"''' % database)
    return res == '1'


def grant_privileges_on_db(database, username):
    run('''
        sudo -i -u postgres psql -t -A -c "GRANT ALL
        PRIVILEGES ON DATABASE %s TO %s"''' % (database, username))


def pg_create_user(username, password):
    run('''psql -t -A -c "CREATE USER %(username)s /
                   WITH PASSWORD '%(password)s';"''')


def pg_create_user(username, password):
    run('''
        sudo -i -u postgres psql -t -A -c
        "CREATE USER %s WITH PASSWORD '%s'"''' % (username, password))


def pg_create_database(database, owner):
    run('sudo -i -u postgres createdb %s -O %s' % (database, owner))


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
            run('source %s/bin/activate && pip install -r requirements.txt' %
                (os.path.abspath(VIRTENV)))


def setup_ngnix():
    run('sudo ln -sf ~%s'
        '/etc/nginx/sites-enabled/' % (os.path.abspath(NGINX_CONF)))
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
