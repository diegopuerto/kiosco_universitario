'''
Created on 15/02/2016

@author: EJArizaR
'''
from apps.services_requests.views.ServicesRequesterBase import ServicesRequestBase
from apps.services_requests.forms import SpecializedChamberForm

class SpecializedChamberRequestView(ServicesRequestBase):
    template_name = "services_requests/specialized_chamber.html"
    request_form = SpecializedChamberForm
    
    def craft_request(self, forms, user):
        request_instance = forms['services_request_form'].save(commit=False)
        request_instance.user = user
        request_instance.service = "Solicitud Sala Especializada"
        request_instance.save()
        return request_instance
    
    def get_subject(self, subject):
        return 'Solicitud Sala Especializada'