from django import template

register = template.Library()


@register.filter
def absolute_create_url(obj):
    """
    Access model's meta data on template.
    :param obj:
    :return:
    """
    return obj._meta.absolute_create_url