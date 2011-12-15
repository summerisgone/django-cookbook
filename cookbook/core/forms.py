# -*- coding: utf-8 -*-
from django import forms
from models import Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CrispyMixin(object):

    def __init__(self, *args, **kwargs):
        super(CrispyMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

class NewProjectForm(CrispyMixin, forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'project_builder',)

class ConfigurationForm(CrispyMixin, forms.Form):

    def __init__(self, recipe, *args, **kwargs):
        super(ConfigurationForm, self).__init__(*args, **kwargs)

        for var in recipe.variables.filter(editable=True):
            self.fields[var.name] = forms.CharField(label=var.description, max_length=255)
