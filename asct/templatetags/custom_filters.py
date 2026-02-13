from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """
    문자열 치환 필터
    사용법: {{ value|replace:"old,new" }}
    예: {{ "hello world"|replace:"world,django" }} -> "hello django"
    """
    if value is None:
        return ""
        
    qs = args.split(',')
    if len(qs) != 2:
        return value
        
    search, replace_with = qs
    return str(value).replace(search, replace_with)