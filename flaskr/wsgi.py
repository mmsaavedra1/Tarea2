import sys
#
## The "/home/moisess" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/moisess/myproject"
path = '/app/Tarea2'
if path not in sys.path:
    sys.path.append(path)
#
from flaskr import create_app
application = create_app()