# -*- coding: utf-8 -*-
from core.helpers import AppRecipe, url_helper


class FlatpagesRecipe(AppRecipe):
    _file = __file__
    appname = 'django.contrib.flatpages'
    installed_apps = [
        'django.contrib.flatpages',
    ]
    middleware_classes = 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'

recipe = FlatpagesRecipe
