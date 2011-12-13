# -*- coding: utf8 -*-
from django.conf.urls.defaults import url, patterns, include, handler404, handler500
{% load buildtags %}

{% get_all_vars 'urls.import' as imports %}
{% for import in imports %}
{{ import }}
{% endfor %}

{% getval 'urls.admin_autodiscover' %}
{% getval 'urls.before_patterns' %}

{% get_all_vars 'urls.patterns' as patterns %}

urlpatterns = patterns('',
{% for pattern in patterns %}
    url(
        '{{ pattern.regex }}', {{ pattern.view|safe }},{% if pattern.name %}name='{{ pattern.name }}',{% endif %}
        {% if pattern.kwargs %}kwargs={{ pattern.kwargs|pprint|safe }},{% endif %}
        {% if pattern.name %}name='{{ pattern.name }}',{% endif %}
        {% if pattern.prefix %}prefix='{{ pattern.prefix }}',{% endif %}
    ),
{% endfor %}
)