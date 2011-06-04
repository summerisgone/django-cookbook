# -*- coding: utf8 -*-
{% load buildtags %}
from settings import *

SECRET_KEY = '{% getval SECRET_KEY %}'

{% allvars INSTALLED_APPS as installed_apps %}
INSTALLED_APPS += [
    {% for var in installed_apps %}
    '{{ var.value }}',
    {% endfor %}
]
