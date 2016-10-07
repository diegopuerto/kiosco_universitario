'''
Created on 17/02/2016

@author: EJArizaR
'''
from apps.services_requests.views.ServicesRequesterBase import ServicesRequestBase
from apps.services_requests.forms import StatisticalCultureForm

class StatisticalCultureRequestView(ServicesRequestBase):
    request_form = StatisticalCultureForm   
    template_name = "services_requests/statistical_culture.html"
    
    def craft_request(self, forms, user):
        request_instance = forms['services_request_form'].save(commit=False)
        request_instance.user = user
        request_instance.save()
        return request_instance

    def get_subject(self, subject):
        return str(subject)