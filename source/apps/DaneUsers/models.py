# -*- coding: utf-8 -*-
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
__author__    = "Orlando Saavedra, Emmanuel Ariza"
__status__    = "Prototype"

from base import settings
from custom_user.models import AbstractEmailUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from libs.django_smart_selects.smart_selects.db_fields import ChainedForeignKey 

class ProfileFieldsBase(models.Model):
    alias = models.CharField(_("Alias"),max_length=120)
    name  = models.CharField(_("Name"),max_length=240)
    def __unicode__(self):
        return self.alias
    
    class Meta:
        abstract = True
    
# Model to manage identification type options.
class IdType(ProfileFieldsBase):
    class Meta:
        verbose_name = _("ID Type")    
        verbose_name_plural = _("ID Types")    

# Model to manage age range options.
class AgeRange(ProfileFieldsBase):
    class Meta:
        verbose_name = _("Age Range")
        verbose_name_plural = _("Age Ranges")

# Model to manage educational options.
class EducationalType(ProfileFieldsBase):
    class Meta:
        verbose_name = _("Educational Type")
        verbose_name_plural = _("Educational Types")
        
# Model to manage professional options.
class ProfessionalType(ProfileFieldsBase):
    class Meta:
        verbose_name = _("Professional Type")
        verbose_name_plural = _("Professional Types")

# Model to manage activity options.
class ActivityType(ProfileFieldsBase):
    class Meta:
        verbose_name = _("Activity Type")
        verbose_name_plural = _("Activity Types")
    
# Model to manage activity options.
class Departament(ProfileFieldsBase):
    class Meta:
        verbose_name = _("Departament")
        
# Model to manage activity options.
class City(ProfileFieldsBase):
    departament = ForeignKey(Departament, null=False)
    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
    
# Model to manage activity options.
class DisabilityType(ProfileFieldsBase):
    class Meta:
        verbose_name = _("Disability Type")
        verbose_name_plural = _("Disability Types")

# Model with extra user information for DANE users
class UserProfile(models.Model):
    GENDER_CHOICES = (
        (None, _("Select gender")),
        (True, _('Male')),
        (False, _('Female'))
    )
    
    user                 = models.OneToOneField(settings.AUTH_USER_MODEL,null=False)
    departament          = models.ForeignKey(Departament,null=False)
    city                 = ChainedForeignKey(City,
                                             chained_field="departament",
                                             chained_model_field="departament", 
                                             show_all=False, 
                                             auto_choose=True,
                                             null=False)
    id_type              = models.ForeignKey(IdType,null=True, blank=True)
    id_doc               = models.CharField(_('ID document'),max_length=30,null=True, blank=True, unique = True) #Required
    cellphone            = models.CharField(_('Cellphone'),max_length=120,null=True, blank=True)
    phone                = models.CharField(_('phone'),max_length=120,null=True, blank=True)
    gender               = models.NullBooleanField(_('Gender'),choices=GENDER_CHOICES,null=True, blank=True, default=None) # Requerido
    age_range            = models.ForeignKey(AgeRange,null=True, blank=True)
    education            = models.ForeignKey(EducationalType,null=True, blank=True)
    activity             = models.ForeignKey(ActivityType,null=True, blank=True)
    profession           = models.ForeignKey(ProfessionalType,null=True, blank=True)
    disability           = models.ForeignKey(DisabilityType,null=True, blank=True)
    country_of_residence = CountryField(blank_label=_('(Select country)'), null=True, blank=True)
    created_on           = models.DateTimeField(_("Created"), auto_now_add=True)
    alternative_mail     = models.EmailField(_('alternative mail'), null = True, blank=True, unique = True)

    
    def clean(self):
        if hasattr(self,"city") and hasattr(self, "departament") and not self.city.departament == self.departament:
            raise ValidationError(_('City and departament are not consistent'))


    def __unicode__(self):
        return "%s (%s)" % (self.fullname, (self.id_doc if self.id_doc else 'None'))
    
    @property
    def fullname(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self), field) for field in UserProfile._meta.fields]
    
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
    
 
class BasicDaneUser(AbstractEmailUser):
    first_name     = models.CharField(_('Names'),max_length=50,null=True) #Required
    last_name      = models.CharField(_('Surnames'),max_length=50,null=True) #Required
    _is_staff      = models.BooleanField(_('Is Staff'), default = False)
    _is_active     = models.BooleanField(_('Is Staff'), default = True)
    key_expires    = models.DateTimeField(default = timezone.now() + datetime.timedelta(days=7))
    is_confirmed   = models.BooleanField(_('Is Confirmed'), default = False)   
    activation_key = models.CharField(max_length=40, null = True) 

    @property
    def is_active(self):
        if self.key_expires < timezone.now() and not self.is_confirmed:
            return False
        else:
            return self._is_active
    
    @is_active.setter
    def is_active(self, value):
        self._is_active =  value
        
    @property
    def is_staff(self):
        return self._is_staff

    @is_staff.setter
    def is_staff(self, value):
        if value and ('servant',) in self.groups.values_list('name'):
            self._is_staff = True
        else:
            self._is_staff = False
  
    class Meta:
        verbose_name = _("User")       
