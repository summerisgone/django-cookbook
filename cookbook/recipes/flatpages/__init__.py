# -*- coding: utf-8 -*-
from core.helpers import AppRecipe, url_helper


class FlatpagesRecipe(AppRecipe):
    appname = 'django.contrib.flatpages'
    installed_apps = [
        'django.contrib.flatpages',
    ]
    middleware_classes = 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'

recipe = FlatpagesRecipe
