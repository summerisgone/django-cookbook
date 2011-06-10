# -*- coding: utf8 -*-
{% load buildtags %}
from settings import *
from os.path import join, dirname

ADMINS = (
    ('admin', 'info@{{ project.domain }}'),
)

MANAGERS = (
    ('manager', 'info@{{ project.domain }}'),
)

EMAIL_SUBJECT_PREFIX = '[{{ project.name }}]'

PROJECT_DIR = dirname(__file__)

{% getval 'settings.DATABASES' as DATABASES %}
DATABASES = {{ DATABASES|pprint|safe }}
SECRET_KEY = '{% getval 'settings.SECRET_KEY' %}'
ROOT_URLCONF = '{{ project.name }}.auto_urls'

MEDIA_URL = '/media/'
MEDIA_ROOT = join(PROJECT_DIR, 'media')

UPLOAD_DIR = 'upload'
UPLOAD_URL = MEDIA_URL + UPLOAD_DIR

# ADMIN_MEDIA_PREFIX = '/media/admin/'

TEMPLATE_DIRS = [join(PROJECT_DIR, 'templates'),]

FIXTURE_DIRS = [join(PROJECT_DIR, 'fixtures'),]

{% get_all_vars 'settings.INSTALLED_APPS' as INSTALLED_APPS %}
INSTALLED_APPS = list(INSTALLED_APPS) + [{% for var in INSTALLED_APPS %}
'{{ var }}',{% endfor %}]

{% get_all_vars 'settings.MIDDLEWARE_CLASSES' as MIDDLEWARE_CLASSES %}
MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [{% for var in MIDDLEWARE_CLASSES %}
'{{ var }}',{% endfor %}]

{% get_all_vars 'settings.CONTEXT_PROCESSORS' as CONTEXT_PROCESSORS %}
CONTEXT_PROCESSORS =  [{% for var in CONTEXT_PROCESSORS %}
'{{ var }}',{% endfor %}]

# FCGI Server settings
FORCE_SCRIPT_NAME = ''
