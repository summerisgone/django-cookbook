# -*- coding: utf-8 -*-
from core.helpers import AppRecipe, url_helper


class DjangoAdminRecipe(AppRecipe):
    appname = 'django.contrib.admin'
    installed_apps = [
        'django.contrib.admin',
        'django.contrib.admindocs',
    ]
    urlpatterns = [
        url_helper(r'^admin/doc/', "include('django.contrib.admindocs.urls')"),
        url_helper(r'^admin/', "include(admin.site.urls)"),
    ]

    def __init__(self, *args, **kwds):
        super(DjangoAdminRecipe, self).__init__(*args, **kwds)
        # Insert autodiscover
        self.vars['urls.import'] = 'from django.contrib import admin'
        self.vars['urls.admin_autodiscover'] = 'admin.autodiscover()'
