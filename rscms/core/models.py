from django.template import loader
from core import tasks
from os.path import join


class Project(object):

    def __init__(self, name, domain, path):
        self.name = name
        self.domain = domain
        self.path = path
        self.recipes = []
        return super(Project, self).__init__()

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

    def get_context(self):
        return {'project': self}

    def render(self):
        for recipe in self.recipes:
            recipe.render()
        return self


class Recipe(object):

    def __init__(self, project, name):
        self.project = project
        self.name = name
        # rendered files and variables
        self.vars = KeyStore(self)
        self.files = []
        # copied folders
        self.raw = []
        return super(Recipe, self).__init__()

    def get_context(self):
        context = self.project.get_context()
        context.update({
            'recipe': self
        })
        return context

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
        return super(RawDirectory, self).__init__()


class KeyStore(dict):

    def __init__(self, recipe, *args, **kwds):
        self.recipe = recipe
        return super(KeyStore, self).__init__(*args, **kwds)


class FileConfig(object):

    def __init__(self, recipe, filename, template):
        self.recipe = recipe
        self.filename = filename
        self.template = template
        return super(FileConfig, self).__init__()

    def render(self, context):
        return loader.render_to_string(self.template, context)
