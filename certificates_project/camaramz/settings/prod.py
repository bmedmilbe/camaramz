import os
import dj_database_url
from .common import *

# --- CORE SETTINGS ---
DEBUG = False
# Use .get() with a fallback to prevent crashes during the Docker build phase
SECRET_KEY = os.environ.get("SECRET_KEY", "temporary-secret-key-for-build")
ALLOWED_HOSTS = ["camaramzapi-6cf2b687304f.herokuapp.com", ".railway.app", ".up.railway.app",
                 "xmambos.com", ".xmambos.com"
                 ]

# --- CORS & CSRF CONFIGURATION ---
CORS_ALLOW_ALL_ORIGINS = False
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CORS_ALLOWED_ORIGINS = [
    "https://cmz.st",
    "https://www.cmz.st",
    "https://cecab.st",
    "https://www.cecab.st",
    "https://cecabnext.vercel.app",
    "https://kandja.vercel.app",

]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
    r"^https://.*\.railway\.app$",
    r"^https://.*\.up\.railway\.app$",
]
# Required for POST/PUT requests in production
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS + [
    "https://*.vercel.app",
    "https://*.railway.app",
    "https://*.up.railway.app",
    "https://xmambos.com",
    "https://www.xmambos.com",
    "https://*.xmambos.com",

]

# HTTPS Security Headers
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CORS_ALLOW_CREDENTIALS = True
# --- DATABASE ---
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

# --- AWS STORAGE ---
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = "eu-north-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False

# --- EMAIL & DOMAIN ---
DOMAIN = os.environ.get("RAILWAY_STATIC_URL", "www.cmz.st")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
MOVED = os.environ.get("MOVED", "False")

# --- MULTI-SITE EMAIL CONFIGURATION ---
WEBSITES = ["CMZ", "ORMED", "CECAB", "NANEHOUSE", "BESPOKETOUR"]

CMZ_PASSWORD = os.environ.get("CMZ_PASSWORD", "")
ORDMEDSTP_PASSWORD = os.environ.get("ORDMEDSTP_PASSWORD", "")
CECABSTP_PASSWORD = os.environ.get("CECABSTP_PASSWORD", "")

EMAILS = {
    WEBSITES[0]: {
        "EMAIL": "edmilbe@gmail.com",
        "TITLE": "CMZ",
        "PASSWORD": CMZ_PASSWORD,
        "WEBSITE": "https://camaramz-cc67c4aaa69f.herokuapp.com/",
        "LOGO": "https://www.camaramezochi.st/files/stp/camara2.png",
    },
    WEBSITES[1]: {
        "EMAIL": "ormedstp@gmail.com",
        "TITLE": "ORDMED-STP",
        "PASSWORD": ORDMEDSTP_PASSWORD,
        "WEBSITE": "https://ormedstp.herokuapp.com/",
        "LOGO": "https://ormedstp.herokuapp.com/images/logo-2.png",
    },
    WEBSITES[2]: {
        "EMAIL": "direcaocecab@gmail.com",
        "TITLE": "CECAB-STP",
        "PASSWORD": CECABSTP_PASSWORD,
        "WEBSITE": "https://www.cecab.st/",
        "LOGO": "https://www.cecab.st/images/logo.png",
    },
    WEBSITES[3]: {
        "EMAIL": "edmilbe@gmail.com",
        "TITLE": "Edmilbe Ramos",
        "PASSWORD": EMAIL_HOST_PASSWORD,
        "WEBSITE": "https://www.edmilbe.pro/",
        "LOGO": "https://edmilbe-fa58f9b99040.herokuapp.com/light/assets/imgs/header/profile.jpg",
    },
}
