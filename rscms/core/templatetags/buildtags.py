from classytags.core import Tag, Options
from classytags.arguments import Argument
from django import template

register = template.Library()


def isiterable(obj):
    return bool(getattr(obj, '__iter__', False))


class GetAllVars(Tag):
    name = 'get_all_vars'
    options = Options(
        Argument('keyname'),
        'as',
        Argument('varname', resolve=False, required=False)
    )

    def render_tag(self, context, keyname, varname):
        project = context['project']
        vars = []
        for recipe in project.recipes:
            if keyname in recipe.vars:
                if isiterable(recipe.vars[keyname]):
                    vars.extend(recipe.vars[keyname])
                else:
                    vars.append(recipe.vars[keyname])

        if varname:
            context[varname] = vars
        else:
            context[keyname] = vars

        return u''

register.tag(GetAllVars)


class GetValue(Tag):
    name = 'getval'
    options = Options(
        Argument('keyname'),
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def render_tag(self, context, keyname, varname):
        project = context['project']
        value = None
        for recipe in project.recipes:
            if keyname in recipe.vars:
                value = recipe.vars[keyname]

        if varname:
            context[varname] = value
            return u''
        else:
            return value

register.tag(GetValue)
