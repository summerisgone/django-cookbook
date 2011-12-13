# -*- coding: utf-8 -*-
from core.models import Project, Variable


class DjangoBuilder(object):
    """
    The initial django project
    """

    def __init__(self, project):
        self.project = project
        super(DjangoBuilder, self).__init__()
