from django.core.management.base import BaseCommand
from os.path import abspath, join, dirname, abspath
import os
from optparse import make_option
from rscms.core.models import Project
from rscms.recipes.base_project.models import BaseProjectRecipe

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

        base_project_recipe = BaseProjectRecipe(project, project.name)
        project.recipes.append(base_project_recipe)

        project.copy_raw()
        project.render()
