from django.test import TestCase
from .forms import CartAddProductForm

class CartAddProductFormTest(TestCase):
        def test_form(self):
                form_data = {'quantity': 1, 'update': True}
                form = CartAddProductForm(data=form_data)
                self.assertTrue(form.is_valid())

