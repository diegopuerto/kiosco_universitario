from django.test import TestCase
from .models import Category

# model test
class CategoryTest(TestCase):

        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def test_create_category(self):
                c = self.create_category()
                self.assertTrue(isinstance(c, Category))
                self.assertEqual(c.__str__(), c.name)
