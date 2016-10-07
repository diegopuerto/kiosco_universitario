# -*- encoding: utf-8 -*-
from django.template.defaulttags import register
from django.views.generic.base import TemplateView

# Create your views here.
class Home(TemplateView):
    
    template_name = "kiosco_app/home.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['forms_urls'] = [{"title":"Formulario Solicitud de Información",
                            "id":"info-request",
                            "url":"http://orfeoott.dane.gov.co/orfeo_3.6.0/radicacionWeb/radicacionPqrs/ingresoPqr.php?rad=1"},
                          {"title":"Formulario Quejas y Reclamos",
                            "id": "complaints",
                           "url":"http://orfeoott.dane.gov.co/orfeo_3.6.0/radicacionWeb/radicacionPqrs/ingresoPqr.php?rad=2"},
                           {"title":"Formulario Derecho de Petición",
                           "id": "petitions",
                            "url":"http://orfeoott.dane.gov.co/orfeo_3.6.0/radicacionWeb/radicacionPqrs/ingresoPqr.php?rad=3"}]
        context['orfeo_follow'] = {"title":"Seguimiento a Radicados",
                            "id" :"following",
                             "url":"http://orfeoott.dane.gov.co/orfeo_3.6.0/consultaWeb/"}
        context['geoportal'] =  {"title":"Geoportal",
                            "id" :"geoportal",
                            "url":"http://geoportal.dane.gov.co/mgn_lite/"}
        context['relay_center']= {"title":"Centro de Reelevo",
                         "id" :"relay-center",
                          "url":"http://200.69.101.70/audarapps/Livechat/Relevos/"}
        context['chat']= {"title":"Chat",
                         "id" :"chat",
                          "url":"http://172.16.128.61/WebChatASP/"}
        return context

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary[key]