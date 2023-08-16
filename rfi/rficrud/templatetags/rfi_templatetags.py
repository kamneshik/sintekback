from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='rfi_templatetags')
def user_groups(user):
    return Group.objects.filter(user=user).values_list('name', flat=True)


@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
