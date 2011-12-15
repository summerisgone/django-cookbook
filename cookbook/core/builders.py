# -*- coding: utf-8 -*-
from random import choice
from core.models import Variable
from os.path import dirname, join
from django.conf import settings
from django.template import Context, Template
import tarfile
import os
import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class DjangoBuilder(object):
    """
    The initial django project
    """

    def __init__(self, project):
        self.project = project
        self.template_dir = join(dirname(__file__), 'templates', 'builders', 'django_base')
        self.init_vars()
        super(DjangoBuilder, self).__init__()

    def init_vars(self):
        secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50)])
        package, _ = Variable.objects.get_or_create(name='package', project=self.project, editable=True)
        package.val = self.project.name
        package.save()

        domain, _ = Variable.objects.get_or_create(name='domain', project=self.project, editable=True)
        domain.val = 'example.com'
        domain.save()

        key, _ = Variable.objects.get_or_create(name='SECRET_KEY', project=self.project)
        key.val = secret_key
        key.editable = False
        key.save()

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
                tar.add(join(root, d), arcname=tar_dirname, recursive=False)

            for f in files:
                if f.endswith('_tmpl'):
                    # render template to tar
                    t = Template(open(join(root, f), 'r').read())
                    rendered = t.render(Context(self.project.to_dict()))

                    tarinfo = tarfile.TarInfo(f.split('_tmpl')[0])
                    tarinfo.size = len(rendered)

                    tar.addfile(tarinfo, StringIO(rendered.encode('utf-8')))
                else:
                    tar_filename = join(rel_root, f)
                    tar.add(join(root, f), arcname=tar_filename)

        tar.close()