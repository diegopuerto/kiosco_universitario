from django.db import models
from base import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.
    

class StatisticalCultureService(models.Model):
    alias = models.CharField(_("Alias"),max_length=120)
    name  = models.CharField(_("Name"),max_length=240)
    def __unicode__(self):
        return self.alias
    
    class Meta:
        verbose_name = _("Statistical Culture Service")    
        verbose_name_plural = _("Statistical Culture Services")    

class BaseServiceRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=False)
    detail = models.TextField(_('detail'))
    is_closed = models.BooleanField(_('Request is closed'),default =False)
    created_on = models.DateTimeField(_("Created"), auto_now_add=True)
    from_ip = models.TextField(_('from ip'))
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    null=True,
                                    limit_choices_to={'is_staff': True},
                                    related_name='+')
    class Meta:
        abstract = True
        
class SpecializedChamberRequest(BaseServiceRequest):
    service = models.CharField(_('service'), max_length=255)
    
    class Meta:
        verbose_name = _("Specialized Chamber Request")    
        verbose_name_plural = _("Specialized Chamber Requests")    

class StatisticalCultureRequest(BaseServiceRequest):
    service = models.ForeignKey(StatisticalCultureService, null=False)
    
    class Meta:
        verbose_name = _("Statistical Culture Request")    
        verbose_name_plural = _("Statistical Culture Requests")    