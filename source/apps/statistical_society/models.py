from django.db import models
from apps.DaneUsers.models import BasicDaneUser
from base import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class StatisticalSocietyMember(BasicDaneUser):
    class Meta:
        proxy = True
        verbose_name = _("Statistical Society Member")    
        verbose_name_plural = _("Statistical Society Members")  

class StatisticalSocietyMemberEmail(BasicDaneUser):
    class Meta:
        proxy = True


class StatisticalSocietyUserPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=False)
    use_of_info = models.CharField(_('use of statistical information'), max_length=120)  
    suscription_media = models.CharField(_('suscription media'), max_length=120)  
    want_cell_messages = models.BooleanField(_('Wants receive cell messages'),max_length=50,default =False)
    want_email_messages = models.BooleanField(_('Wants receive email messages'),max_length=50,default =False)
    pib_info = models.BooleanField(_('gross domestic product'),max_length=50,default =False)
    ipc_info = models.BooleanField(_("consumer's price index"),max_length=50,default =False)
    ipp_info = models.BooleanField(_("producer's price index"),max_length=50,default =False)
    workforce_info = models.BooleanField(_("Global Participation Rate / Rate occupation / Unemployment Rate / percent of working age population"),max_length=50,default =False)
    imports_info = models.BooleanField(_("imports"),max_length=50,default =False)    
    exports_info = models.BooleanField(_("exports"),max_length=50,default =False)    
    mmcm_info = models.BooleanField(_("sample monthly retail"),max_length=50,default =False)    
    mmm_info = models.BooleanField(_("monthly manufacturing sample"),max_length=50,default =False)    
    

    
    