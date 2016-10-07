from django.contrib import admin
from apps.services_requests.models import StatisticalCultureService,\
    SpecializedChamberRequest, StatisticalCultureRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


# Register your models here.
    
class service_request_admin_base(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('detail', 'service')}),
        (_('User'), {'fields': ("user", )}),
        (_('Important dates'), {'fields': ('created_on','from_ip')}),
        (_('Assigned to'), {'fields': ("assigned_to", 'is_closed')}),
    )
    readonly_fields = ('created_on', 'from_ip') 
    list_filter = ("is_closed",
                   )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(email=request.user.email)
        return super(admin.ModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(StatisticalCultureService)
admin.site.register(SpecializedChamberRequest, service_request_admin_base)
admin.site.register(StatisticalCultureRequest, service_request_admin_base)