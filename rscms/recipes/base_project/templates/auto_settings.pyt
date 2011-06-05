# -*- coding: utf8 -*-
{% load buildtags %}
from settings import *

SECRET_KEY = '{% getval 'settings.SECRET_KEY' %}'

{% get_all_vars 'settings.INSTALLED_APPS' as INSTALLED_APPS %}

INSTALLED_APPS += [
    {% for var in INSTALLED_APPS %}
    '{{ var }}',  # {{ var.key }}
    {% endfor %}
]
