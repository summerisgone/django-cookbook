from settings import *

{% allkeys INSTALLED_APPS as installed_apps %}
INSTALLED_APPS += [
    {% for keyconfig in installed_apps %}
    '{{ keyconfig.value }}',
    {% endfor %}
]
