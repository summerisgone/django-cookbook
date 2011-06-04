from rscms.core.models import Recipe, RawDirectory, FileConfig
from django.template import loader
from django.template.base import TemplateDoesNotExist
from os.path import abspath, join, dirname, abspath
import os
import django


class BaseProjectRecipe(Recipe):

    requirement = 'django'
    templates = [
        'auto_settings.pyt',
        'auto_urls.pyt',
    ]

    def __init__(self, project, appname):
        requirement = 'django'
        super(BaseProjectRecipe, self).__init__(project, appname, requirement)
        self.prepare_rendered()
        self.prepare_raw()

    def prepare_rendered(self):
        for template in self.templates:
            try:
                loader.find_template(template)
            except TemplateDoesNotExist:
                pass
            else:
                target_filename = template.replace('.pyt', '.py')
                self.files.append(FileConfig(self, target_filename, template))

    def prepare_raw(self):
        target_dir = self.project.path
        # Append default project folder from django
        django_template_dir = os.path.join(django.__path__[0], 'conf', 'project_template')
        self.raw.append(RawDirectory(self, django_template_dir, target_dir))

        # Append raw folder in module
        module_raw_dir = join(dirname(abspath(__file__)), 'raw')
        self.raw.append(RawDirectory(self, module_raw_dir, target_dir))
