'''
Created on 23/10/2015

@author: ejarizar
'''
from apps.DaneUsers.views.ProfileManagerView import ProfileManagerMixinView
from apps.statistical_society.forms import SEPreferencesForm
from django.contrib.auth import get_user_model
from apps.statistical_society.models import StatisticalSocietyUserPreference
from django.contrib.auth.models import Group
    
    
class RegisterSEUserView(ProfileManagerMixinView):

    template_name = "statistical_society/register.html"
    user_preferences_form = "user_preferences_form"
    
    def get_form_classes(self, user):
        forms = ProfileManagerMixinView.get_form_classes(self, user)
        forms[self.user_preferences_form] = SEPreferencesForm
        return forms
    
    def get_forms(self, form_classes, request):
        forms = ProfileManagerMixinView.get_forms(self, form_classes, request)
        if isinstance(request.user, get_user_model()) and StatisticalSocietyUserPreference.objects.filter(user=request.user).exists():
            forms[self.user_preferences_form] = form_classes[self.user_preferences_form](instance=StatisticalSocietyUserPreference.objects.get(user=request.user), **self.get_form_kwargs())
        return forms
    
    def save(self, forms, request):
        if not request.user.is_authenticated():
            user_form = forms['user_form']
            user = user_form.save()
            ProfileManagerMixinView.save(self, forms, request)
        else:
            user = request.user
        if isinstance(user, get_user_model()):
            statistical_society_user_group = Group.objects.get(name='statistical_society_user')
            statistical_society_user_group.user_set.add(user)
        data_instance = forms[self.user_preferences_form].save(commit=False)
        data_instance.user = user
        data_instance.save()
        
    def are_forms_valid(self, forms):
        return forms[self.user_preferences_form].is_valid()
    
    def get_context_data(self, **kwargs):
        context = super(RegisterSEUserView, self).get_context_data(**kwargs)
        if context["forms"]["user_form"].instance.pk is not None:
            context["userProfile"] = context["forms"]["user_profile_form"].instance
        return context