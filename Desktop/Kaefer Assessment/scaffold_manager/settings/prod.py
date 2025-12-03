from .base import *
import os

# Production specific settings
DEBUG = False

# Load ALLOWED_HOSTS from environment variable, split by comma
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if '' in ALLOWED_HOSTS:
    ALLOWED_HOSTS.remove('') # Remove empty string if no ALLOWED_HOSTS is set

# Secret key should be loaded from environment variable in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-production-fallback')
if SECRET_KEY == 'a-very-secret-key-for-production-fallback':
    import warnings
    warnings.warn("SECRET_KEY not set in environment variable. Using a fallback value. This is insecure for production!", RuntimeWarning)

# Use secure cookies in production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True # Ensure this is handled by your Azure setup or Nginx/Apache in front

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# This is where Django will collect static files to for deployment
STATIC_ROOT = BASE_DIR / 'staticfiles'

# You might need to configure WhiteNoise or another service to serve static files
# For Azure App Service, it typically serves static files from STATIC_ROOT

# Example for WhiteNoise (install with pip install whitenoise)
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
