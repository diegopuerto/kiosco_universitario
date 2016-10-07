'''
Created on 23/12/2015

@author: EJArizaR
'''

#WARNING: NOT TESTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from django import template
register = template.Library()
@register.filter
def klass(ob):
    return ob.__class__.__name__
