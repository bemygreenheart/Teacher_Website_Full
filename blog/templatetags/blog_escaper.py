from django import template

register = template.Library()

@register.filter()
def myescaper(value):
  start = value.find('>')
  if start > 0 and start < 100:
    value = value[start+1: ]
  return value

