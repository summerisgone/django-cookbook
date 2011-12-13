# -*- coding: utf-8 -*-
from random import choice
from core.models import Variable


class DjangoBuilder(object):
    """
    The initial django project
    """

    def init_vars(self):
        secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50)])
        Variable.objects.create(name='package', val=self.project.name, project=self.project)
        Variable.objects.create(name='SECRET_KEY', val=secret_key, project=self.project)

    def __init__(self, project):
        self.project = project
        self.init_vars()
        super(DjangoBuilder, self).__init__()
