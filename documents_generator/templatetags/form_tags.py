from django import template

register = template.Library()

@register.filter
def add_label_class(field):
    return field.label_tag(attrs={"class": "form-label"})