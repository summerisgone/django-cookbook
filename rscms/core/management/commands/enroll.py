from django.core.management.base import BaseCommand
from os.path import abspath, join, dirname, abspath
import os
from optparse import make_option
from rscms.core.models import Project
import recipes

class Command(BaseCommand):
    help = "Test site build"
    option_list = BaseCommand.option_list + (
        make_option('-n', '--name', action='store', dest='project_name', default='mysite',
            help='Project python module name'),
        make_option('-d', '--domain', action='store', dest='domain', default='example.com',
            help='Project domain'),
    )
    args = ''

    def handle(self, *args, **options):
        os.getcwd()

        project_path = join(os.getcwd(), options['project_name'])
        # New project
        project = Project(name=options['project_name'], domain=options['domain'],
            path=project_path)

        recipes.autodiscover()

        base_recipe = recipes.registry.get_base_recipe()(project, project.name)
        project.recipes.append(base_recipe)

        for RecipeCls in recipes.registry.all():
            project.recipes.append(RecipeCls(project))

        project.copy_raw()
        project.render()
