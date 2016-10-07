'''
Created on 18/09/2015

@author: EJArizaR
'''
from libs.django_auth_ldap.config import LDAPSearch

class DaneLDAPSearch(LDAPSearch):
    def execute(self, connection, filterargs=(), escape=True):
        results = super(DaneLDAPSearch, self).execute(connection, filterargs=filterargs, escape=escape)        
        return results

class UserNotFoundError(ValueError):
    pass