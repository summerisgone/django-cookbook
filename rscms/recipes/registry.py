from core.models import Recipe


class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class RecipeRegistry(object):
    _registry = {}

    def register(self, recipe):
        if hasattr(recipe, 'name'):
            recipename = recipe.name
        else:
            recipename = recipe.appname
        if recipename in self._registry:
            raise AlreadyRegistered
        else:
            self._registry[recipename] = recipe

    def unregister(self, appname_or_recipe):
        if issubclass(appname_or_recipe, Recipe):
            try:
                del self._registry[appname_or_recipe.name]
            except KeyError:
                raise NotRegistered
        else:
            try:
                del self._registry[appname_or_recipe]
            except KeyError:
                raise NotRegistered

    def get_recipe(self, name):
        return self._registry.get(name, None)

    def get_base_recipe(self):
        return self._registry.get(None, None)

    def all(self):
        for key in self._registry.keys():
            if key:
                yield self.get_recipe(key)
