# -*- coding: utf8 -*-
from django.conf.urls.defaults import url, patterns

{% load buildtags %}
{% get_all_vars 'urls.patterns' as patterns %}

urlpatterns = patterns('',
{% for pattern in patterns %}
    url('{{ pattern.regex }}', {{ pattern.view|safe }}, {% if pattern.name %}name='{{ pattern.name }}'{% endif%}),
{% endfor %}
)