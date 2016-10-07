'''
Created on 17/09/2015

@author: EJArizaR
'''
from libs.django_auth_ldap.backend import LDAPBackend
from django.contrib.auth.models import Group

class DaneLDAPBackend(LDAPBackend):
    
    def authenticate(self, email, password, **kwargs):      
        username, server = email.strip().split("@")
        if server.lower() == "dane.gov.co":

            user = super(DaneLDAPBackend, self).authenticate(username, password)
        else:
            user = None
        return user
      
    def populate_user(self, email):
        username= email.strip().split("@")[0]
        user = super(DaneLDAPBackend, self).populate_user(username)
        if not user == None:
            full_name = user.ldap_user.attrs["displayname"][0]
            user.first_name = full_name.split()[0]
            user.last_name = full_name.split()[-2]
            user.save()
            servant = Group.objects.get(name='servant')
            servant.user_set.add(user)
        return user    
    
    def get_or_create_user(self, username, ldap_user):
        email = username + "@dane.gov.co"
        return super(DaneLDAPBackend, self).get_or_create_user(email, ldap_user)

class NonExistentLDAPUser():
    pass