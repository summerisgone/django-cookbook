# -*- coding: utf-8 -*- 
from core.models import RawDirectory, Recipe, FileConfig
from django.template import loader
from os.path import join, dirname, abspath, exists, isdir
import os


def url_helper(regex, view, kwargs=None, name=None, prefix=''):
    url = {
        'regex': regex,
        'view': view,
    }
    if kwargs is not None:
        url['kwargs'] = kwargs
    if name is not None:
        url['name'] = name
    if prefix is not None:
        url['prefix'] = prefix
    return url

class AppRecipe(Recipe):
    requirements = []  # ['foo', 'bar ==2.0']
    installed_apps = []  # ['myapp',]
    templates = []  # ['auto_settings.pyt', 'templates/app/base.html']
#    more complicated:
#    urlpatterns = [
#        url_helper(r'myapp/(\d+)', 'myapp.view.object_view', name='myapp_object_view'),
#    ]
    urlpatterns = None

    def __init__(self, project, appname):
        super(AppRecipe, self).__init__(project, appname)
        self.find_raw_folder()
        self.find_templates()
        self.init_vars()

    def find_raw_folder(self):
        target_dir = self.project.path
        # Append raw folder in module
        raw_dirname = join(dirname(abspath(__file__)), 'raw')
        if exists(raw_dirname) and isdir(raw_dirname):
            self.raw.append(RawDirectory(self, raw_dirname, target_dir))

    def find_templates(self):
        for template in self.templates:
            t = loader.get_template(template)

            target_filename = template.replace('.pyt', '.py')
            target_filename = os.path.join(*target_filename.split('/'))  # Windows cases
            self.files.append(FileConfig(self, target_filename, t.name))

    def init_vars(self):
        if self.requirements:
            if self.requirements:
                self.vars['requirements'] = self.requirements
            if self.installed_apps:
                self.vars['settings.INSTALLED_APPS'] = self.installed_apps
            if self.urlpatterns:
                self.vars['urls.patterns'] = self.urlpatterns
