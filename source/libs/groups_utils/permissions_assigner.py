'''
Created on 16/10/2015

@author: EJArizaR
'''
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class PermissionsAssigner(object):
    '''
    classdocs
    '''

    DELETE = "delete_"
    ADD = "add_"
    CHANGE = "change_"


    def __init__(self):
        '''
        Constructor
        '''

    
    def set_permissions(self, group, modelname, permission):
        contenttype = ContentType.objects.get(model=modelname)
        permission = Permission.objects.get(content_type=contenttype, codename=permission + modelname)
        group.permissions.add(permission)

    
    
        