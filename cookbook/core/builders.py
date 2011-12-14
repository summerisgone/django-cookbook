# -*- coding: utf-8 -*-
from random import choice
from core.models import Variable
from os.path import dirname, join
from django.conf import settings
import os
import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import tarfile

class DjangoBuilder(object):
    """
    The initial django project
    """

    def __init__(self, project):
        self.project = project
        self.template_dir = join(dirname(__file__), 'templates', 'django_base')
        self.init_vars()
        super(DjangoBuilder, self).__init__()

    def init_vars(self):
        secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50)])
        Variable.objects.create(name='package', val=self.project.name, project=self.project)
        Variable.objects.create(name='domain', val='example.com', project=self.project)
        Variable.objects.create(name='SECRET_KEY', val=secret_key, project=self.project)

    def render_dirname(self, d):
        regexp = '.*\+([a-zA-Z][a-zA-Z0-9_]+)\+.*'
        match = re.match(regexp, d)
        tar_dirname = d
        if match:
            varname = match.groups()[0]
            value = str(self.project[varname])
            if value:
                tar_dirname = re.sub(regexp, value, d)
        return tar_dirname

    def build(self):
        filename = join(settings.UPLOAD_ROOT, 'projects', 'project-%s.tar.gz' % self.project.pk)
        reldir = self.template_dir

        # Prepare output structure
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        if os.path.exists(filename):
            os.remove(filename)

        tar = tarfile.TarFile.open(filename, 'w:gz')

        # TODO: build recipes at first

        for root, dirs, files in os.walk(self.template_dir):
            rel_root = root.split(self.template_dir)[1]
            rel_root = self.render_dirname(rel_root)

            for d in dirs:
                tar_dirname = join(rel_root, self.render_dirname(d))

                print 'Add directory ', tar_dirname
                tar.add(join(root, d), arcname=tar_dirname, recursive=False)

            for f in files:
                tar_filename = join(rel_root, f)
                print 'Add file ', tar_filename
                tar.add(join(root, f), arcname=tar_filename)

        tar.close()