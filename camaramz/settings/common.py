import os
from pathlib import Path
from datetime import timedelta
import socket
# --- PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE SETTINGS ---
ROOT_URLCONF = "camaramz.urls"
WSGI_APPLICATION = "camaramz.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = False

# --- APPS ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "djoser",
    "certificates",
    "troca",
    "cms",
    "setup",
    "core",
    "storages",
    "mail_templated",
    "debug_toolbar",
    "drf_spectacular",
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.TenantMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Handles local static files
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# --- AUTHENTICATION & USER ---
AUTH_USER_MODEL = "core.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- TENANT ---
TENANT_MODEL = "core.Tenant"

AUTHENTICATION_BACKENDS = [
    'core.backends.TenantEmailOrPhoneBackend',
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# --- HYBRID STORAGE CONFIGURATION ---
# This setup separates static and media
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",  # User uploads -> S3
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # CSS/JS -> Local
    },
}

# WhiteNoise settings
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
WHITENOISE_IGNORE_MISSING_FILES = True

CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "credentials",
    "x-tenant-id"
]

CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False

# --- REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_METADATA_CLASS': None,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "COERCE_DECIMAL_TO_STRING": False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Government Multi-Tenant Kernel API',
    'DESCRIPTION': (
        'Centralized Backend Engine for Municipal Management and NGO Services. '
        'Includes Analytical & Automation Workflows for document issuance (CMZ) '
        'and supply chain transparency (CECAB). Featuring strict Tenant isolation '
        'and Financial Ledger integrity.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Edmilbe Ramos',
        'email': 'bm.edmilbe@gmail.com',
    },
    # Garante que a documentação use o esquema de autenticação correto (ex: JWT ou Token)
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_COMMAND': True,
}

# Spectacular Settings atualizado para JWT
SPECTACULAR_SETTINGS = {
    'TITLE': 'Government Multi-Tenant Kernel API',
    'DESCRIPTION': (
        'Centralized Backend Engine for Municipal Management and NGO Services. '
        'Analytical & Automation Workflows with JWT Authentication and Tenant isolation.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Edmilbe Ramos',
        'email': 'bm.edmilbe@gmail.com',
    },
    'APPEND_COMPONENTS': {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    'SECURITY': [
        {
            "BearerAuth": [],
        }
    ],
}
# --- DJOSER & JWT ---
DJOSER = {
    "SET_PASSWORD_RETYPE": True,
    "SET_USERNAME_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "auth/reset-password/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    'LOGIN_FIELD': 'email',
    'USER_ID_FIELD': 'id',
    "SERIALIZERS": {
        "user_create": "core.serializers.UserCreateSerializer",
        "user": "core.serializers.UserSerializer",
        "current_user": "core.serializers.UserSerializer",
        "token_create": "core.serializers.TenantTokenObtainPairSerializer",
        "set_password_retype": "core.serializers.SetPasswordRetypeSerializer",
        "set_username": "core.serializers.SetUsernameSerializer",
        "password_reset": "core.serializers.SendEmailResetSerializer",
        "password_reset_confirm_retype": "core.serializers.PasswordResetConfirmRetypeSerializer",
    },



}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_PAIR_SERIALIZER": 'core.serializers.TenantTokenObtainPairSerializer',
}

# --- EMAIL SETTINGS ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "edmilbe@gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ADMINS = [("Ramos", "admin@hotmail.com")]

# --- LOGGING ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {name} - {message}",
            "style": "{",
        }
    },
}
