# -*- coding: utf8 -*-
{% load buildtags %}
from settings import *

SECRET_KEY = '{% getval 'settings.SECRET_KEY' %}'

ROOT_URLCONF = '{{ project.name }}.auto_urls'

{% getval 'settings.DATABASES' as DATABASES %}
DATABASES = {{ DATABASES|pprint|safe }}

{% get_all_vars 'settings.INSTALLED_APPS' as INSTALLED_APPS %}
INSTALLED_APPS = [{% for var in INSTALLED_APPS %}
'{{ var }}',{% endfor %}]

{% get_all_vars 'settings.MIDDLEWARE_CLASSES' as MIDDLEWARE_CLASSES %}
MIDDLEWARE_CLASSES = [{% for var in MIDDLEWARE_CLASSES %}
'{{ var }}',{% endfor %}]

{% get_all_vars 'settings.CONTEXT_PROCESSORS' as CONTEXT_PROCESSORS %}
CONTEXT_PROCESSORS = [{% for var in CONTEXT_PROCESSORS %}
'{{ var }}',{% endfor %}]
