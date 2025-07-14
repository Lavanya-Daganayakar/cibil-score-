"""
Django settings for cibil_prediction project
===========================================

✓ Works out-of-the-box for local development.
✓ Uses SQLite, DEBUG=True, static files under <project-root>/static.
✓ Looks for templates in <project-root>/templates plus each app’s templates/.

Switch DEBUG to False, set a real SECRET_KEY, add ALLOWED_HOSTS,
and move to Postgres/MySQL before deploying to production.
"""

from pathlib import Path

# ────────────────────────────────────────────────────────────────
# Base directory
# ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ────────────────────────────────────────────────────────────────
# Security
# ────────────────────────────────────────────────────────────────
SECRET_KEY = "⚠️  REPLACE-THIS-WITH-A-SECURE-SECRET-KEY"
DEBUG = True                      # set False in production
ALLOWED_HOSTS: list[str] = []     # e.g. ["127.0.0.1", "example.com"]

# ────────────────────────────────────────────────────────────────
# Application definition
# ────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "predictor",
    # Third-party apps (add here later, e.g. "rest_framework")
]

# Any model *without* an explicit PK will get BigAutoField:
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cibil_prediction.urls"

# ────────────────────────────────────────────────────────────────
# Templates
# ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # project-level templates folder:
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,   # also look inside <app>/templates/
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cibil_prediction.wsgi.application"

# ────────────────────────────────────────────────────────────────
# Database (SQLite for dev)
# ────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ────────────────────────────────────────────────────────────────
# Password validation
# ────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ────────────────────────────────────────────────────────────────
# Internationalization
# ────────────────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ────────────────────────────────────────────────────────────────
# Static & media files
# ────────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]   # dev assets live here
STATIC_ROOT = BASE_DIR / "staticfiles"     # `collectstatic` target (prod)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ────────────────────────────────────────────────────────────────
# Logging (simple console logging)
# ────────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ────────────────────────────────────────────────────────────────
# Place any third-party or custom settings below
# e.g. REST_FRAMEWORK = { ... }
# ────────────────────────────────────────────────────────────────
