# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

from views import NewProjectView, FrontpageView


urlpatterns = patterns('core.views',
    url(r'^$', FrontpageView.as_view(), name='frontpage'),
    url(r'^new/$', NewProjectView.as_view(), name='new_project'),
    url(r'^build/(\d{1,4})/$', 'build_project', name='build_project'),
)
