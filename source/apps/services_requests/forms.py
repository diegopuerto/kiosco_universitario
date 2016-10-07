'''
Created on 1/12/2015

@author: EJArizaR
'''
from apps.services_requests.models import SpecializedChamberRequest,\
    StatisticalCultureRequest
from apps.DaneUsers.forms import ModelCssClassForm
from django import forms
from apps.services_requests import models
from django.utils.translation import ugettext_lazy as _

class ServicesRequestForm(ModelCssClassForm):
    class Meta:
        model = SpecializedChamberRequest
        exclude = ("user",)
        
class SpecializedChamberForm(ServicesRequestForm):
    class Meta:
        model = SpecializedChamberRequest
        fields = ["detail"]
        exclude = ("user", "service")
        
class StatisticalCultureForm(ServicesRequestForm):
    service = forms.ModelChoiceField(models.StatisticalCultureService.objects.all(),empty_label= _("(Statistical culture service)"))
    class Meta:
        model = StatisticalCultureRequest
        fields = ["detail", "service"]
        exclude = ("user",)    