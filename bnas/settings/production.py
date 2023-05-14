from .base import *


DEBUG = bool(os.environ.get("DEBUG", False))
ALLOWED_HOSTS = ['.herokuapp.com', 'manosunidas.heroku.com', 'locashost', '127.0.0.1']


# DATABASES = {
#     "default": {
#         "ENGINE": 'django.db.backends.postgresql_psycopg2',
#         "NAME": 'd7robaue0qtvs5',
#         "USER": 'xokcepuulrjemg',
#         "PASSWORD": 'cc14d1740aafb778314e327661d85d8e3230e5c31a64f27e1681cf57272360ad',
#         "HOST": 'ec2-3-225-110-188.compute-1.amazonaws.com',
#         "PORT": '5432',

#     }
# }

DATABASES = {
    "default": {
        "ENGINE":env("POSTGRES_ENGINE"),
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("PG_HOST"),
        "PORT": env("PG_PORT"),

    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]