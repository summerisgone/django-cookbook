from core.importpath import importpath
from recipes.store import RecipeRegistry, AlreadyRegistered
__all__ = ['admin', 'base_project', 'flatpages', ]


registry = RecipeRegistry()

def autodiscover():
    for mod in __all__:
        try:
            registry.register(importpath('recipes.' + mod + '.recipe'))
        except (ImportError, AlreadyRegistered):
            pass
