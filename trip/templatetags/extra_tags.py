from django import template

register = template.Library()

@register.filter
def get_name_at_index(list, index):
    return list[index - 1].name

@register.filter
def get_period_at_index(list, index):
    return list[index - 1].period

@register.filter
def get_id_at_index(list, index):
    return list[index - 1].id

@register.filter
def index_exist(list, index):
    if len(list) >= index:
        return True
    return False