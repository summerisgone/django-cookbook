# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from builders import DjangoBuilder
from views import NewProjectView


urlpatterns = patterns('core.views',
#    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', NewProjectView.as_view(), name='new_project'),
    url(r'^build/(\d{1,4})/$', 'build_project', name='build_project'),
)
