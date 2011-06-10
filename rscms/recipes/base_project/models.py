# -*- coding: utf-8 -*-
from core.helpers import AppRecipe, db_helper
from core.models import RawDirectory
from os.path import join
from random import choice
import django


class BaseProjectRecipe(AppRecipe):

    _file = __file__
    requirements = 'django'
    templates = [
        'auto_settings.pyt',
        'auto_urls.pyt',
        'requirements.txt'
    ]
    urlpatterns = []
    context_processors = []
    middleware_classes = []


    def __init__(self, project, appname, database='sqlite3'):
        super(BaseProjectRecipe, self).__init__(project, appname)

        # Generate secret key
        self.vars['settings.SECRET_KEY'] = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

        # Append default project folder from django
        target_dir = self.project.path
        django_template_dir = join(django.__path__[0], 'conf', 'project_template')
        self.raw[0:0] = (RawDirectory(self, django_template_dir, target_dir),)

        # configure databases
        if type(database) is dict:
            self.vars['settings.DATABASES'] = database
        elif database == 'sqlite3':
            self.vars['settings.DATABASES'] = {'default': db_helper(self.project, 'sqlite3')}
        elif database == 'postgresql':
            self.vars['settings.DATABASES'] = {'default': db_helper(self.project, 'postgresql')}
        elif database == 'mysql':
            self.vars['settings.DATABASES'] = {'default': db_helper(self.project, 'mysql')}
        elif database == 'oracle':
            self.vars['settings.DATABASES'] = {'default': db_helper(self.project, 'oracle')}
