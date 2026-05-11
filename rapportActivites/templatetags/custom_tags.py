from django import template

register = template.Library()

@register.filter
def remplacer(value, args):
    try:
        old, new = args.split(',')
        return str(value).replace(old, new)
    except:
        return value
    
    
@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name, None)