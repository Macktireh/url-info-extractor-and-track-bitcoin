from config.env import BASE_DIR, DjangoEnvironment, env, env_to_enum

env.read_env(env_file=BASE_DIR.parent / ".env")

DJANGO_ENV = env_to_enum(
    enum_cls=DjangoEnvironment, value=env.str(var="DJANGO_ENV", default=DjangoEnvironment.LOCAL)
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(var="DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DJANGO_ENV == DjangoEnvironment.LOCAL

ALLOWED_HOSTS = env.list(var="ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])


# Application definition
LOCAL_APPS = [
    "apps.common",
    "apps.accounts",
    "apps.urlinfo",
]

THIRD_PARTY_APPS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DJANGO_ENV != DjangoEnvironment.PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR.parent / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env.str(var="DB_ENGINE"),
            "NAME": env.str(var="DB_NAME"),
            "USER": env.str(var="DB_USER"),
            "PASSWORD": env.str(var="DB_PASSWORD"),
            "HOST": env.str(var="DB_HOST"),
            "PORT": env.int(var="DB_PORT"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"


# Django admin
DJANGO_ADMIN_PATH_NAME = env.str(var="DJANGO_ADMIN_PATH_NAME", default="admin/")
