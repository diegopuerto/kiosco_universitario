# -*- coding: utf-8 -*- 
'''
Created on 2/12/2015

@author: EJArizaR
'''

class UserInfoExtractor(object):
    
    


    def _get_atribute_recursively(self, user, field):
        path = field.split(".")
        if len(path) == 1:
            return unicode(getattr(user, field))
        else:
            return self._get_atribute_recursively(getattr(user, path[0]), ".".join(path[1:]))

    def _get_info_from_fields(self, user, fields):
        info = ""
        for field in fields:
            info = info + field.split(".")[-1] + ": " +  self._get_atribute_recursively(user, field) + "\n"
        return info
    

    def extract(self, user):
        return self._get_info_from_fields(user, ["first_name",
                                                 "last_name",
                                                 "email",
                                                 "userprofile.id_type",
                                                 "userprofile.id_doc",
                                                 "userprofile.cellphone",
                                                 "userprofile.age_range",
                                                 "userprofile.country_of_residence",
                                                 "userprofile.education",
                                                 "userprofile.activity",
                                                 "userprofile.profession",
                                                 ])

