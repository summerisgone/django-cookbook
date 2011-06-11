from core.models import FileConfig
import core.tasks
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from os.path import dirname, exists, join
import os
import recipes


class Command(BaseCommand):
    help = "Creates new recipe"
    option_list = BaseCommand.option_list + (
#        make_option('-i', '--interactive', action='store_false', dest='interactive',
#            help='Interactive mode'),
    )
    args = 'recipe_name'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Recipe name required')
        self.recipe_name = args[0]
        default_options = {
            'create_raw': True,
            'appname': self.recipe_name,
            'create_urlpatterns': True,
            'middleware_classes': [],
            'templates': [],
            'requirements': [],
            'installed_apps': [],
        }

        # TODO: interactive mode

        self.create_recipe(default_options)

    def classname(self):
        name = self.recipe_name
        return name[0].upper() + name[1:] + 'Recipe'

    def create_recipe(self, options):
        recipes_dir = dirname(recipes.__file__)
        target_dir = join(recipes_dir, self.recipe_name)
        if exists(target_dir):
            raise CommandError('Recipe %s already exists!' % self.recipe_name)
        # Create folder
        os.mkdir(target_dir)
        # Render __init__.py file
        options['classname'] = self.classname()
        recipe_file = FileConfig(None, join(target_dir, '__init__.py'), 'recipe.pyt')
        core.tasks.write_file(recipe_file.filename, recipe_file.render(options))
        # Render raw and templates if needed
        if options['create_raw']:
            os.makedirs(join(target_dir, 'raw'))
        if options['templates']:
            os.makedirs(join(target_dir, 'templates'))
        for template in options['templates']:
            open(join(target_dir, 'templates', template), 'w').close()
