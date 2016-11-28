from django.test import TestCase
from .models import Category, Product
from datetime import datetime

# model test
class CategoryTest(TestCase):

        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def test_create_category(self):
                c = self.create_category()
                self.assertTrue(isinstance(c, Category))
                self.assertEqual(c.__str__(), c.name)

class CategoryTestReverse(TestCase):

        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def test_validate_reverse_category(self):
                c = self.create_category()
                self.assertTrue(isinstance(c, Category))
                self.assertEqual(c.get_absolute_url(), '/shop/exportaciones-colombia/')


class ProductTest(TestCase):


        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def create_product(self, category="", name="exportaciones_bolivia", slug="exportaciones-bolivia", description="exportaciones a Bolivia", available="True", created=datetime.now(), updated=datetime.now()):
                return Product.objects.create(category=category, name=name, slug=slug, description=description, available=available, created=created, updated=updated)


        def test_create_product(self):
                c = self.create_category()
                p = self.create_product(category=c)
                self.assertTrue(isinstance(p, Product))
                self.assertEqual(p.__str__(), p.name)
