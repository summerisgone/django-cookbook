from django.template import loader
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from core import tasks
from os.path import join


VARIABLE_TYPE_STRING = 0
VARIABLE_TYPE_UNICODE = 1
VARIABLE_TYPE_LIST = 2
VARIABLE_TYPE_DICT = 3
VARIABLE_TYPE_OTHER = -1
VARIABLE_TYPE_CHOICES = (
    ('String', VARIABLE_TYPE_STRING),
    ('Unicode string', VARIABLE_TYPE_UNICODE),
    ('List', VARIABLE_TYPE_LIST),
    ('Dictionary', VARIABLE_TYPE_DICT),
    ('Other', VARIABLE_TYPE_OTHER),
)

PROJECT_BUILDER_DJANGO = 0
PROJECT_BUILDER_CHOICES = (
    ('Django project', PROJECT_BUILDER_DJANGO),
)

RECIPE_BUILDER_APP = 0
RECIPE_BUILDER_CHOICES = (
    ('Django app', RECIPE_BUILDER_APP),
)

package_valid_name = RegexValidator(regex='^[a-zA-Z][a-zA-Z0-9_]+$',
        message='Should be a valid python package name')

variable_valid_name = RegexValidator(regex='^[a-zA-Z0-9_]+$',
        message='Should be a valid python variable name')


class Project(models.Model):

    name = models.CharField('Project name', max_length=16,
        validators=[package_valid_name])
    description = models.CharField('Project description', max_length=255)
    project_builder = models.IntegerField('Project builder', choices=PROJECT_BUILDER_CHOICES)
    download = models.FileField('Download project archive',
        upload_to=join(settings.UPLOAD_ROOT, 'projects'), null=True, blank=True)

    def render(self):
        for recipe in self.recipes:
            recipe.cook()
        return self


class Requirement(models.Model):

    requires = models.CharField('Depends on these packages', max_length=255)
    recommends = models.CharField('Recommends these packages', max_length=255)
    replaces = models.CharField('Replaces these packages', max_length=255)
    suggests = models.CharField('Suggests to use these packages', max_length=255)


class Recipe(models.Model):

    project = models.ForeignKey(Project, related_name='recipes')
    # TODO: Insert choices fetch into constructor
    provided_package = models.CharField('Provided package', max_length=100,
        validators=[package_valid_name])
    recipe_template = models.IntegerField('Recipe builder', choices=RECIPE_BUILDER_CHOICES)
    templates = models.FileField('Archive with templates for recipe',
        upload_to=join(settings.UPLOAD_ROOT, 'templates'))
    # Metadata:
    author = models.ForeignKey('auth.User')
    requirements = models.OneToOneField(Requirement)

    def cook(self):
        pass


class Variable(models.Model):

    project = models.ForeignKey(Project, related_name='variables')
    recipe = models.ForeignKey(Recipe, null=True, blank=True, related_name='variables')
    name = models.CharField('Variable name', max_length=255,
        validators=[variable_valid_name])
    description = models.CharField('Meaning of variable', max_length=255,
        null=True, blank=True)
    val = models.CharField('Value', max_length=255, null=True, blank=True)
    var_type = models.IntegerField('Variable type',
        choices=VARIABLE_TYPE_CHOICES, default=VARIABLE_TYPE_STRING)