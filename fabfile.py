import random
from fabric.contrib.files import append, exists
from fabric.context_managers import settings
from fabric.api import cd, env, local, run, sudo


DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PSWD = os.environ['DB_PSWD']
REPO_URL = 'https://github.com/samstudy/37_transcendence_1.git'
PROJECT_FOLDER = '/opt/webapps/37'
VIRTENV_FOLDER = '/opt/myenv/37_task'


def prepare_packages():
    run("sudo apt-get update")
    run("sudo apt-get upgrade")
    run("sudo sudo apt-get install build-essential "
        "libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip")
    run("sudo apt-get install python3-pip python3-dev "
        "libpq-dev postgresql postgresql-contrib nginx")
    run("sudo pip3 install --upgrade pip")
    run("sudo apt-get install python-virtualenv")
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


def install_git_and_clone_repo():
    with settings(warn_only=True):
        res = run('which git')
    if res == '/usr/bin/git':
        print('Git allready installed')
    else:
        run("mkdir %s" % (GIT_FOLDER))
        with cd(GIT_FOLDER):
            run('wget https://github.com/git/git/archive/v2.8.1.zip '
                '-O git.zip')
            run('unzip git.zip')
            with cd('git-*'):
                run('make prefix=/usr/local all')
                run('make prefix=/usr/local install')
    run('rm -rf %s' % (PROJECT_FOLDER))
    run('mkdir %s' % (PROJECT_FOLDER))
    with cd(PROJECT_FOLDER):
        run('git clone %s' % (REPO_URL))


def create_virt():
    run('sudo virtualenv %s' % (VIRTENV_FOLDER))
    run('source %s/bin/activate' % (VIRTENV_FOLDER))
    with cd(PROJECT_FOLDER):
        with cd('37_*'):
            run('pip install -r requirements.txt')


def setup_ngnix():
    run('sudo /etc/init.d/nginx start')
    run('sudo ln -s ~/opt/webapp/37_transcendence_1/nginx_conf '
        '/etc/nginx/sites-enabled/')
    run('python manage.py collectstatic')
    run('sudo /etc/init.d/nginx restart')


def fab_bootstrap():
    prepare_packages()
    if not is_pg_user_exists(DB_USER):
        pg_create_user(DB_USER, DB_PSWD)
    if not is_pg_database_exists(DB_NAME):
        pg_create_database(DB_NAME, DB_USER)
    grant_privileges_on_db(DB_NAME, DB_USER)
    install_git_and_clone_repo()
    create_virt()
    setup_ngnix()
