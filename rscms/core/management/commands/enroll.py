from django.core.management.base import BaseCommand
from rscms.core.models import Site
from rscms.recipes.base_project.models import BaseProjectRecipe
from os.path import abspath

class Command(BaseCommand):
    help = "Test site build"
    option_list = (
        make_option('-n', '--name', action='store', dest='project_name', default='mysite',
            help='Project python module name'),
        make_option('-d', '--domain', action='store', dest='domain', default='example.com',
            help='Project domain'),
    )
    args = ''

    def handle(self, *args, **options):
        project_path = join(dirname(abspath(__file__)), options['name'])

        # New project
        project = Project(name=options['name'], domain=options['domain'],
            path=project_path)

#        base_project_recipe = BaseProjectRecipe()
#        project.recipes += base_project_recipe


        project.prepare().copy_raw().render()
