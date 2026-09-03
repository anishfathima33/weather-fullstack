"""
Django settings for weather_project project.
"""

from pathlib import Path
from datetime import timedelta
import environ
import os

# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------

env = environ.Env(
    DEBUG=(bool, False)
)

ENV_FILE = BASE_DIR.parent / ".env"

if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)


# --------------------------------------------------
# SECURITY
# --------------------------------------------------

SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-change-this-in-production"
)

DEBUG = env(
    "DEBUG",
    default=False
)


# --------------------------------------------------
# ALLOWED HOSTS
# --------------------------------------------------

ALLOWED_HOSTS = [
    "weather-fullstack-1.onrender.com",
    "localhost",
    "127.0.0.1",
]


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "corsheaders",

    # Local apps
    "accounts",
    "weather_app",
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [

    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
]


# --------------------------------------------------
# URL / WSGI
# --------------------------------------------------

ROOT_URLCONF = "weather_project.urls"

WSGI_APPLICATION = "weather_project.wsgi.application"


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.postgresql",

        "NAME": env("DB_NAME", default="weather_app"),

        "USER": env("DB_USER", default="postgres"),

        "PASSWORD": env("DB_PASSWORD", default=""),

        "HOST": env("DB_HOST", default="localhost"),

        "PORT": env("DB_PORT", default="5432"),
    }
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# OPENWEATHER
# --------------------------------------------------

OPENWEATHER_API_KEY = env(
    "OPENWEATHER_API_KEY",
    default=""
)


# --------------------------------------------------
# EMAIL
# --------------------------------------------------

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = env(
    "EMAIL_HOST",
    default="smtp.gmail.com"
)

EMAIL_PORT = env(
    "EMAIL_PORT",
    default=587
)

EMAIL_USE_TLS = env(
    "EMAIL_USE_TLS",
    default=True
)

EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    default=""
)

EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    default=""
)

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="noreply@weatherapp.com"
)


# --------------------------------------------------
# DJANGO REST FRAMEWORK
# --------------------------------------------------

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": (

        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ),

    "DEFAULT_PERMISSION_CLASSES": (

        "rest_framework.permissions.AllowAny",

    ),
}


# --------------------------------------------------
# JWT
# --------------------------------------------------

SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME":
        timedelta(hours=1),

    "REFRESH_TOKEN_LIFETIME":
        timedelta(days=7),

    "ROTATE_REFRESH_TOKENS":
        False,

    "BLACKLIST_AFTER_ROTATION":
        False,

    "UPDATE_LAST_LOGIN":
        False,

    "ALGORITHM":
        "HS256",

    "SIGNING_KEY":
        SECRET_KEY,

    "VERIFYING_KEY":
        None,

    "AUTH_HEADER_TYPES":
        ("Bearer",),

    "AUTH_HEADER_NAME":
        "HTTP_AUTHORIZATION",

    "USER_ID_FIELD":
        "id",

    "USER_ID_CLAIM":
        "user_id",

    "TOKEN_TYPE_CLAIM":
        "token_type",

    "AUTH_TOKEN_CLASSES":
        (
            "rest_framework_simplejwt.tokens.AccessToken",
        ),

    "TOKEN_OBTAIN_SERIALIZER":
        "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",

    "TOKEN_REFRESH_SERIALIZER":
        "rest_framework_simplejwt.serializers.TokenRefreshSerializer",

}


# --------------------------------------------------
# CORS
# --------------------------------------------------

CORS_ALLOWED_ORIGINS = [

    "https://weather-fullstack-nu.vercel.app",

    "http://localhost:5173",

    "http://localhost:5174",

    "http://localhost:5175",

]

CORS_ALLOW_CREDENTIALS = True


# --------------------------------------------------
# CSRF
# --------------------------------------------------

CSRF_TRUSTED_ORIGINS = [

    "https://weather-fullstack-nu.vercel.app",

    "http://localhost:5173",

    "http://localhost:5174",

    "http://localhost:5175",

]


# --------------------------------------------------
# CACHE
# --------------------------------------------------

CACHES = {

    "default": {

        "BACKEND":
            "django.core.cache.backends.locmem.LocMemCache",

        "LOCATION":
            "weather-cache",

        "OPTIONS": {

            "MAX_ENTRIES":
                1000,

        },
    },
}