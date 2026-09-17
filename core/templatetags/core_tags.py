from django import template
register = template.Library()

@register.filter
def percentage_color(value):
    """Returns a CSS color class based on percentage value"""
    try:
        v = float(value)
        if v >= 80: return 'text-success'
        elif v >= 50: return 'text-warning'
        else: return 'text-danger'
    except: return 'text-muted'

@register.filter  
def truncate_words_custom(value, num):
    words = str(value).split()
    if len(words) > int(num):
        return ' '.join(words[:int(num)]) + '...'
    return value
