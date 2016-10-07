from django.views.generic.edit import FormMixin, ProcessFormView

class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    """
    form_classes = {} # set the form classes as a mapping

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes, request):
        return dict([(key, klass(**self.get_form_kwargs())) \
            for key, klass in form_classes.items()])

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms, next=self.request.GET.get('next',None)))


class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that processes multiple forms on POST. Every form must be
    valid.
    """
    def get(self, request, *args, **kwargs):
        form_classes = self.form_classes
        forms = self.get_forms(form_classes, request)
        return self.render_to_response(self.get_context_data(forms=forms, next=request.GET.get('next',None)))

    def post(self, request, *args, **kwargs):
        form_classes = self.form_classes
        forms = self.get_forms(form_classes, request)
        if self.are_forms_valid(forms):
            return self.forms_valid(forms, request)
        else:
            return self.forms_invalid(forms)

    def are_forms_valid(self, forms):
        return all([form.is_valid() for form in forms.values()])

class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

    def forms_valid(self, forms, request = None):
        self.save(forms, request)
        return MultipleFormsMixin.forms_valid(self, forms)
    
    def save(self, forms, request=None):
        raise NotImplementedError

    