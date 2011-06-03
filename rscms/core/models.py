from django.db import models
from django.template import loader
from defer import defer

class Project(object):

    def __init__(self, name, domain, path):
        self.name = name
        self.domain = domain
        self.path = path
        self._recipes = []
        return super(self, Project).__init__()

    def get_recipes(self):
        return self._recipes

    def set_recipes(self, value):
        self._recipes = value

    # Use getter-setter for foreign keys future hooks
    recipes = property(get_recipes, set_recipes, None, 'Installed recipes')

    def build(self):
        for app in self.get_apps():
            for fileconfig in app.get_files():
                fileconfig.render(app, self)

    def prepare(self):
        '''Prepare folder structure'''
        return self

    def copy_raw(self):
        for recipe in self.recipes:
            recipe.copy_raw()
        return self

    def render(self):
        for recipe in self.recipes:
            recipe.render()
        return self


class Recipe(object):

    def __init__(self, project, appname, requirement):
        self.project = project
        self.name = appname
        self.requirement = requirement
        self.keys = []
        self.files = []
        self.raw = []
        return super(self, Recipe).__init__()

    def get_context(self):
        return {'recipe': self}

    def copy_raw(self):
        defers = []
        for raw in self.raw:
            defers.append(tasks.copy_folder(raw.source,
                join(self.project.path, raw.target)))
        return defers

    def render(self):
        defers = []
        for fileconfig in self.files:
            content = fileconfig.render(self.get_context())
            defers.append(tasks.write_file(join(self.project.path,
                fileconfig.filename), content))
        return defers


class RawDirectory(object):

    def __init__(self, recipe, source, target):
        self.recipe = recipe
        self.source = source
        self.target = target
        return super(self, RawDirectory).__init__()


class KeyConfig(object):

    def __init__(self, recipe, key, value):
        self.recipe = recipe
        self.key = key
        self.value = value
        return super(self, KeyConfig).__init__()


class KeyStore(dict):

    def __init__(self, recipe, *args, **kwds):
        self.recipe = recipe
        return super(self, KeyStore).__init__(*args, **kwds)


class FileConfig(object):

    def __init__(self, recipe, filename, template):
        self.recipe = recipe
        self.filename = filename
        self.template = template
        return super(self, FileConfig).__init__()

    def render(self, context):
        return loader.render_to_string(self.template, context)
