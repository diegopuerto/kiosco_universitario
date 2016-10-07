from django.contrib import admin
from models import UserProfile, ActivityType, IdType, AgeRange,\
    EducationalType, ProfessionalType, BasicDaneUser, Departament, City
from custom_user.admin import EmailUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.options import StackedInline
# Register your models here.i
    
class ProfileInLine(StackedInline):
    model = UserProfile
            
    def get_formset(self, request, obj=None, **kwargs):
        if obj and "servant" not in obj.groups.values_list('name', flat=True):
            kwargs['exclude'] = ['alternative_mail',]
        return super(ProfileInLine, self).get_formset(request, obj, **kwargs)



class BasicDaneUserAdmin(EmailUserAdmin):
    inlines = [ProfileInLine]    
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ((
        None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
    ),)
    

class ProfileAdmin(admin.ModelAdmin):
#     def get_formset(self, request, obj=None, **kwargs):
#         if obj and "servant" not in obj.groups.values_list('name', flat=True):
#             kwargs['exclude'] = ['alternative_mail',]
#         return super(ProfileInLine, self).get_formset(request, obj, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if obj and "servant" not in obj.user.groups.values_list('name', flat=True):
            self.exclude = ("alternative_mail", )
        form = super(ProfileAdmin, self).get_form(request, obj, **kwargs)
        return form

admin.site.register(IdType)
admin.site.register(AgeRange)
admin.site.register(EducationalType)
admin.site.register(ProfessionalType)
admin.site.register(ActivityType)
admin.site.register(Departament)
admin.site.register(City)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(BasicDaneUser, BasicDaneUserAdmin)

