import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#calling os.path.dirname() removes another layer so that BASE_DIR coontains h:/tango_with_django_project/
#print(__file__)
#print(os.path.dirname(__file__))
#print(os.path.dirname(os.path.dirname(__file__)))

#Create a new varaible called TEMPLATE_DIR that will reference your new template director
#make use of os.path.join() to mash together the base_DIR method variable and templates
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

#Create a new variable called STATIC_DIR at the top of settings.py preferably underneath BASE_DIR and templates_DIR
STATIC_DIR = os.path.join(BASE_DIR, 'static')

#Create a new variables for media files
MEDIA_DIR = os.path.join(BASE_DIR, 'media')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w&m(pe-fwa=h24^2ipsd5jf9g815q^4h1j@6sbpgx1nh_(snie'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pictaroo',
    'registration', #add in the registration package Chapter 11

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'IT_team_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #Update the DIRs key/value pairing
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'IT_team_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

#Add two more variables, the root and URL
MEDIA_ROOT = MEDIA_DIR

MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [STATIC_DIR, ]

# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'

# If True, users can register
REGISTRATION_OPEN = True
# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7
# If True, the user will be automatically logged in.
REGISTRATION_AUTO_LOGIN = True
# The page you want users to arrive at after they successfully log in
#REVISIT THIS ---> NEED TO REDIRECT TO THE PROFILE PAGE.
LOGIN_REDIRECT_URL = '/pictaroo/'

# The page users are directed to if they are not logged in,
# and are trying to access pages requiring authentication
LOGIN_URL = '/accounts/login/'