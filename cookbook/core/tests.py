"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test.client import Client
from django.test import TestCase


class DjangoEmptyProject(TestCase):

    def setUp(self):
        pass

    def test_django_builder(self):
        from core.models import Project, PROJECT_BUILDER_DJANGO
        from core.builders import DjangoBuilder
        project = Project(name='test_project', project_builder=PROJECT_BUILDER_DJANGO)
        builder = DjangoBuilder(project)

