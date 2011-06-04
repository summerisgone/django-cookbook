from classytags.core import Tag, Options
from classytags.arguments import Argument
from django import template

register = template.Library()

class AllVars(Tag):
    name = 'allvars'
    options = Options(
        Argument('keyname'),
        'as',
        Argument('varname', resolve=False)
    )

    def render_tag(self, context, keyname, varname):
        project = context['project']
        vars = []
        for recipe in project.recipes:
            vars.extend(filter(lambda s: s.key == keyname, recipe.vars))
        context[varname] = vars
        return u''

register.tag(AllVars)


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
            if keyname in [var.key for var in recipe.vars]:
                value = recipe.vars[keyname]

        if varname:
            context[varname] = value
            return u''
        else:
            return unicode(value)

register.tag(GetValue)
