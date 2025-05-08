import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()  # 🔑 Load environment variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # React app development server
    'http://127.0.0.1:3000',
    'http://10.0.2.2:3000',   # For Android emulator access to local server
]

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-default-key')  # Use environment variable for production
DEBUG = os.getenv("DEBUG", "True") == "True"  # Set to False in production
ALLOWED_HOSTS = ['127.0.0.1', '10.0.2.2', 'localhost']  # Add domains as required

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',

    # Custom apps
    'users',
    'products',
    'orders',
    'prescriptions',
    'coupons',
    'notifications',
    'ai_assistant',
    'settings',
    'rest_framework_simplejwt.token_blacklist',
    # Optional: Add-ons
    'dal',  # django-autocomplete-light
    'dal_select2',
]

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=150),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Handle CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medzy.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Optional custom template directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'medzy.wsgi.application'

# Custom User model
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Razorpay API credentials (use environment variables in production)
RAZORPAY_API_KEY = os.getenv("RAZORPAY_API_KEY", 'rzp_test_GY4iJFc1dQJzvQ')
RAZORPAY_API_SECRET = os.getenv("RAZORPAY_API_SECRET", 'Jwb2JZb3lsJnzrCUROE92mF8')

# OneSignal credentials
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", 'a86e1582-24f8-4aeb-b12d-fe50369d3284')
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY", 'NmI2MTg3YzQtYjdlYy00MDQ0LTgyN2QtZWU1ZWQ4NmQwZDBh')

