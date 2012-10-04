#
# Used to easily deploy code to the production server
#
# INSTALL fabric ON YOUR LOCAL MACHINE
# i.e. sudo easy_install fabric
#
from fabric.api import *

env.hosts=['<production>']

PROJECT_DIR = ''

def deploy():
    project_dir = PROJECT_DIR
    with cd(project_dir):
        run("sudo git pull origin master")

