from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, url_pattern):
    request = context['request']
    if url_pattern in request.path:
        return 'active'
    return 'in-active'

@register.simple_tag(takes_context=True)
def is_show(context, url_pattern):
    request = context['request']
    if url_pattern in request.path:
        return "show"
    return ""
