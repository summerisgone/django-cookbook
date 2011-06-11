from recipes.registry import RecipeRegistry
from core.importpath import importpath

__all__ = ['admin', 'base_project', 'flatpages']


registry = RecipeRegistry()

def autodiscover():
#    recipes_module = __import__('recipes')
    for mod in __all__:
        try:
            registry.register(importpath('recipes.' + mod + '.recipe'))
        except ImportError:
            pass
