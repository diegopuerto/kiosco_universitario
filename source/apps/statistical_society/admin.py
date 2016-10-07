# -*- coding: utf-8 -*-
from apps.statistical_society.models import StatisticalSocietyMember, StatisticalSocietyUserPreference,\
    StatisticalSocietyMemberEmail
from custom_user.admin import EmailUserAdmin
from apps.DaneUsers.admin import ProfileInLine
from apps.statistical_society.forms import StatisticalSocietyUserForm  
from django.contrib.admin.options import StackedInline
from import_export.admin import ExportActionModelAdmin
from django.contrib import admin
from import_export import resources
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _
from import_export.formats import base_formats
from libs.StatisticalSocietyUsersExporterUtils.Formatter import Formatter

class StatisticalSocietyMembersExports(resources.ModelResource):
    class Meta:
        model = StatisticalSocietyMemberEmail
        fields = ("email", "userprofile__cellphone")
        
class StatisticalSocietyProfileInLine(StackedInline):
    model = StatisticalSocietyUserPreference

#WARNING!!!!:  NOT TESTED
class StatisticalSocietyInfoExporterAdmin(ExportActionModelAdmin):
    formatter = Formatter()
    def export_emails_action(self, request, queryset):
        file_format = base_formats.CSV()
        export_data = self.formatter.email_format((self.get_export_data(file_format, queryset)))
        response = HttpResponse(export_data, 'text/txt')
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            "emails.txt",
        )
        return response
        return None
  
    export_emails_action.short_description = _(
        'Export emails from selected %(verbose_name_plural)s')

    def export_cellphones_action(self, request, queryset):
        file_format = base_formats.CSV()
        export_data = self.formatter.cellphone_format((self.get_export_data(file_format, queryset)))
        response = HttpResponse(export_data, 'text/txt')
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            "cellphones.txt",
        )
        return response
        return None
  
    export_cellphones_action.short_description = _(
        'Export cellphones from selected %(verbose_name_plural)s')

    actions = [export_emails_action, export_cellphones_action]
    resource_class =  StatisticalSocietyMembersExports
    
    
class StatisticalSocietyMembersAdmin(EmailUserAdmin, StatisticalSocietyInfoExporterAdmin):
    inlines = [ProfileInLine, StatisticalSocietyProfileInLine]    
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
    )
    add_fieldsets = ((
        None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', "password1", "password2" )
        }
    ),)
#     add_form = StatisticalSocietyUserForm
      
    list_filter = ('statisticalsocietyuserpreference__want_cell_messages',
                   'statisticalsocietyuserpreference__want_email_messages',
                   'statisticalsocietyuserpreference__pib_info',
                   'statisticalsocietyuserpreference__ipc_info',
                   'statisticalsocietyuserpreference__ipp_info',
                   'statisticalsocietyuserpreference__workforce_info',
                   'statisticalsocietyuserpreference__imports_info',
                   'statisticalsocietyuserpreference__exports_info',
                   'statisticalsocietyuserpreference__mmcm_info',
                   'statisticalsocietyuserpreference__mmm_info',
                   )
    
    def get_queryset(self, request):
        qs = EmailUserAdmin.get_queryset(self, request)
        return qs.filter(groups__name='statistical_society_user')
    
    class Media:
        css = {
             'all': ('css/statistical_society_users_admin_list_change.css',)
        }

admin.site.register(StatisticalSocietyMember, StatisticalSocietyMembersAdmin)