import dj_database_url
from ._base import *

DATABASES = {
    "default": dj_database_url.config(),
}

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ALLOWED_HOSTS = ["*"]
DEBUG = False
