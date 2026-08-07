import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


# Checks the 'ENV_MODE' variable in your .env file.
CURRENT_MODE = os.environ.get("ENV_MODE", "production")

# --- LOGIC TO PREVENT DOUBLE PRINTING ---
# We only print if:
# 1. It is the "Child" process (RUN_MAIN='true') which runs the actual server.
# 2. OR we are running a different command (like 'migrate') that doesn't use the watcher.
SHOW_LOGS = (os.environ.get("RUN_MAIN") == "true") or ("runserver" not in sys.argv)

if CURRENT_MODE == "local":
    if SHOW_LOGS:
        print("LOG: Running in LOCAL mode.")
    DEBUG = os.environ.get("LOCAL_DEBUG") == "True"
    ALLOWED_HOSTS = os.environ.get("LOCAL_ALLOWED_HOSTS").split(",")

    DB_NAME = os.environ.get("LOCAL_DB_NAME")
    DB_USER = os.environ.get("LOCAL_DB_USER")
    DB_PASS = os.environ.get("LOCAL_DB_PASSWORD")
    DB_HOST = os.environ.get("LOCAL_DB_HOST")
    DB_PORT = os.environ.get("LOCAL_DB_PORT")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("LOCAL_RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("LOCAL_RECAPTCHA_PRIVATE_KEY")


elif CURRENT_MODE == "production":
    if SHOW_LOGS:
        print("LOG: Running in PRODUCTION SERVER mode.")
    # Default server settings
    DEBUG = os.environ.get("PROD_DEBUG") == "True"
    ALLOWED_HOSTS = os.environ.get("PROD_ALLOWED_HOSTS").split(",")

    DB_NAME = os.environ.get("PROD_DB_NAME")
    DB_USER = os.environ.get("PROD_DB_USER")
    DB_PASS = os.environ.get("PROD_DB_PASSWORD")
    DB_HOST = os.environ.get("PROD_DB_HOST")
    DB_PORT = os.environ.get("PROD_DB_PORT")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("PROD_RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("PROD_RECAPTCHA_PRIVATE_KEY")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-fallback-key")

# Allow Django to trust real client IP from proxy/load balancer
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "import_export",
    "first_app"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ImageWebsite.urls"
AUTH_USER_MODEL = "first_app.UserAccount"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR1, 'HtmlWebsite', 'Html'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'first_app.views.global_footer',
            ],
        },
    },
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "savarnapragya181751@gmail.com"

WSGI_APPLICATION = "ImageWebsite.wsgi.application"

# --- 5. DATABASE CONFIGURATION ---

# Check if we specifically requested SQLite in the .env file
USE_SQLITE = os.environ.get("USE_SQLITE") == "True"

if USE_SQLITE:
    # Option A: Use SQLite (Zero Install)
    if SHOW_LOGS:
        print("LOG: Using SQLite database.")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Option B: Use PostgreSQL (Standard)
    if SHOW_LOGS:
        print("LOG: Using PostgreSQL database.")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASS,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
            "CONN_MAX_AGE": 60,
        }
    }

# Cache Database
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cognilume_cache_table',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# This is where collectstatic puts files (The destination)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# This is where your custom files ARE RIGHT NOW (The source)
# Based on your previous code, they are in 'HtmlWebsite' inside your project
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'HtmlWebsite'),
]
GEOIP_PATH = os.path.join(BASE_DIR, "GeoIP")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
X_FRAME_OPTIONS = 'SAMEORIGIN'

# ==============================================================================
# --- SECURITY & SESSION SETTINGS (Session Hijacking Prevention) ---
# ==============================================================================

# 1. Enforce HTTPS-only cookies (Only applied in Production so local dev still works)
IS_PRODUCTION = CURRENT_MODE == "production"

SESSION_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION

# 2. XSS & CSRF Protection
SESSION_COOKIE_HTTPONLY = True      # Prevents JS from reading the cookie
SESSION_COOKIE_SAMESITE = 'Lax'     # Mitigates Cross-Site Request Forgery

# 3. Session Timeouts
SESSION_COOKIE_AGE = 1800           # Session expires after 30 minutes (1800 seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # Force expiry on browser close

# 4. HTTP Strict Transport Security (HSTS) - Only applied in Production
if IS_PRODUCTION:
    SECURE_HSTS_SECONDS = 31536000  # Enforce HTTPS for 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True