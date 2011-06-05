# -*- coding: utf-8 -*-
from core.helpers import AppRecipe, url_helper
from core.models import RawDirectory
from os.path import join
import django


class BaseProjectRecipe(AppRecipe):

    requirements = 'django'
    templates = [
        'auto_settings.pyt',
        'auto_urls.pyt',
        'requirements.txt'
    ]
    installed_apps = ['django.contrib.admin', 'django.contrib.admindoc']
    urlpatterns = [
        url_helper(r'^admin/doc/', "include('django.contrib.admindocs.urls')"),
        url_helper(r'^admin/', "include(admin.site.urls)"),
    ]

    def __init__(self, project, appname):
        super(BaseProjectRecipe, self).__init__(project, appname)

        # Append default project folder from django
        target_dir = self.project.path
        django_template_dir = join(django.__path__[0], 'conf', 'project_template')
        self.raw.append(RawDirectory(self, django_template_dir, target_dir))
