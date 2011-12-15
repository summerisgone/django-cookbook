# -*- coding: utf-8 -*-
from core.tasks import write_project
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from core.builders import DjangoBuilder
from core.models import Project, PROJECT_BUILDER_DJANGO
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from forms import ConfigurationForm
from django.views.generic.edit import CreateView
from forms import NewProjectForm


class NewProjectView(CreateView):
    model = Project

    def get_form_class(self):
        return NewProjectForm

    def get_success_url(self):
        return reverse('build_project', args=[self.object.pk,])

def build_project(request, object_id):
    project = get_object_or_404(Project, id=object_id)
    if project.project_builder == PROJECT_BUILDER_DJANGO:
        # Create variables
        builder = DjangoBuilder(project)

    if request.method == 'POST':
        form = ConfigurationForm(project, request.POST)
        if form.is_valid():
            builder.build()
            return TemplateResponse(request, 'core/build_success.html', {'project': project})
    else:
        form = ConfigurationForm(project)

    return TemplateResponse(request, 'core/build.html', {'form': form, 'project': project})