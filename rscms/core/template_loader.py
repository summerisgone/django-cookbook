"""
Load tempaltes from recipes
"""
from core.importpath import importpath
from os.path import join, dirname, abspath, exists, isdir
from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader
from django.utils._os import safe_join
import recipes



class Loader(Loader):
    is_usable = True

    def get_template_sources(self, template_name, _=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        recipes.autodiscover()
        template_dirs = []
        base_recipe = recipes.registry.get_base_recipe()
        module = (importpath(base_recipe.__module__))
        template_dir = join(dirname(module.__file__), 'templates')
        if exists(template_dir) and isdir(template_dir):
            template_dirs.append(template_dir)

        for recipe in recipes.registry.all():
            module = (importpath(recipe.__module__))
            template_dir = join(dirname(module.__file__), 'templates')
            if exists(template_dir) and isdir(template_dir):
                template_dirs.append(template_dir)

        print 'Search in dirs:', template_dirs

        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass


_loader = Loader()
