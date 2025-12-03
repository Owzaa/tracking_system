from .base import *

# Development specific settings
DEBUG = True

ALLOWED_HOSTS = []

# Django will complain if CSRF_TRUSTED_ORIGINS is not set for production-like environments
# For development, we can keep it empty or specify localhost
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1']

# You might want to use a different database for development, e.g., an in-memory SQLite database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'dev_db.sqlite3',
#     }
# }
