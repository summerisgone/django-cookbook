# -*- coding: utf-8 -*-
from core.helpers import AppRecipe, url_helper


class {{ classname }}(AppRecipe):
    appname = '{{ appname }}'
    installed_apps = {{ installed_apps|pprint|safe }}
    middleware_classes = {{ middleware_classes|pprint|safe }}
    templates = {{ templates|pprint|safe }}
    requirements = {{ requirements|pprint|safe }}
    {% if create_urlpatterns %}
    urlpatterns = [
        url_helper(r'^{{ appname }}/', "include('{{ appname }}.urls')"),
    ]
    {% endif %}

recipe = {{ classname }}
