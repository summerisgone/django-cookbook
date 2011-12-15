# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse

def index(request):
    return TemplateResponse(request, 'index.html', {'title': 'Title!'})