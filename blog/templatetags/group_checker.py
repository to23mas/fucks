from django import template

register = template.Library()

@register.filter
def is_maintainer(user):
    return user.groups.filter(name='maintainer').exists()
