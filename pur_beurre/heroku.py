from .settings import *

import django_heroku


DEBUG = False
ALLOWED_HOSTS = ["sebastienz.herokuapps.com"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

django_heroku.settings(locals())
