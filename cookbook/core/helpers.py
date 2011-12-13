# -*- coding: utf-8 -*- 
from core.importpath import importpath
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

def db_helper(project, engine_name, dbname=None, user=None, password=None, host=None, port=None):
        engine_config = {}
        if engine_name == 'sqlite3':
            engine_config['ENGINE'] = 'django.db.backends.sqlite3'
            if dbname:
                engine_config['NAME'] = dbname
            else:
                engine_config['NAME'] = project.name + '.sqlite'
        else:
            if user:
                engine_config['USER'] = user
            else:
                engine_config['USER'] = project.name
            if dbname:
                engine_config['NAME'] = dbname
            else:
                engine_config['NAME'] = project.name
            if host:
                engine_config['HOST'] = host
            else:
                engine_config['HOST'] = ''
            if port:
                engine_config['PORT'] = port
            else:
                engine_config['PORT'] = ''

            if engine_name == 'postgresql_psycopg2':
                engine_config['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
            if engine_name == 'postgresql':
                engine_config['ENGINE'] = 'django.db.backends.postgresql'
            elif engine_name == 'mysql':
                engine_config['ENGINE'] = 'django.db.backends.mysql'
            elif engine_name == 'oracle':
                engine_config['ENGINE'] = 'django.db.backends.oracle'
        return engine_config
        if self.requirements:
            self.vars['requirements'] = self.requirements
        if self.installed_apps:
            self.vars['settings.INSTALLED_APPS'] = self.installed_apps
        if self.middleware_classes:
            self.vars['settings.MIDDLEWARE_CLASSES'] = self.middleware_classes
        if self.context_processors:
            self.vars['settings.CONTEXT_PROCESSORS'] = self.context_processors
        if self.urlpatterns:
            self.vars['urls.patterns'] = self.urlpatterns
