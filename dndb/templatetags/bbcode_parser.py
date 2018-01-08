import re
from django import template
import bbcode
from django.core.urlresolvers import reverse_lazy, reverse

register = template.Library()

parser = bbcode.Parser()
parser.add_simple_formatter('character', '<a href="/character/%(value)s">%(value)s</a>')
parser.add_simple_formatter('location', '<a href="/location/%(value)s">%(value)s</a>')
parser.add_simple_formatter('task', '<a href="/task/%(value)s">%(value)s</a>')
parser.add_simple_formatter('item', '<a href="/item/%(value)s">%(value)s</a>')

@register.filter(name='parse_bbcode')
def parse_bbcode(value):
	return parser.format(value)