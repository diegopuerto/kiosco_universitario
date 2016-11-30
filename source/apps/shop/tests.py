from django.test import TestCase
from .models import Category, Product
from datetime import datetime
from django.core.urlresolvers import reverse
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

class ProductTestReverse(TestCase):

        
        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def create_product(self, category="", name="exportaciones_bolivia", slug="exportaciones-bolivia", description="exportaciones a Bolivia", available="True", created=datetime.now(), updated=datetime.now()):
                return Product.objects.create(category=category, name=name, slug=slug, description=description, available=available, created=created, updated=updated)

        def test_validate_reverse_category(self):
                c = self.create_category()
                p = self.create_product(category=c)
                self.assertTrue(isinstance(c, Category))
                self.assertTrue(isinstance(p, Product))
                self.assertEqual(p.get_absolute_url(), '/shop/1/exportaciones-bolivia/')


#########view's tests####################################################

class ProductListTest(TestCase):

        
        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def create_product(self, category="", name="exportaciones_bolivia", slug="exportaciones-bolivia", description="exportaciones a Bolivia", available="True", created=datetime.now(), updated=datetime.now()):
                return Product.objects.create(category=category, name=name, slug=slug, description=description, available=available, created=created, updated=updated)

        def test_product_list(self):
                c = self.create_category()
                p = self.create_product(category=c)
                self.assertTrue(isinstance(c, Category))
                self.assertTrue(isinstance(p, Product))
                response = self.client.get(reverse('shop:product_list'))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context['category'], None)
                self.assertQuerysetEqual(response.context['categories'], ['<Category: exportaciones>'])
                self.assertQuerysetEqual(response.context['products'], ['<Product: exportaciones_bolivia>'])

class ProductListCategoryTest(TestCase):

        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def create_category_other(self, name="exportaciones_uno", slug="exportaciones-europa"):
                return Category.objects.create(name=name, slug=slug)


        def create_product(self, category="", name="exportaciones_bolivia", slug="exportaciones-bolivia", description="exportaciones a Bolivia", available="True", created=datetime.now(), updated=datetime.now()):
                return Product.objects.create(category=category, name=name, slug=slug, description=description, available=available, created=created, updated=updated)

        def create_product_other(self, category="", name="exportaciones_argentina", slug="exportaciones-argentina", description="exportaciones a Argentina", available="True", created=datetime.now(), updated=datetime.now()):
                return Product.objects.create(category=category, name=name, slug=slug, description=description, available=available, created=created, updated=updated)

        def test_product_list_with_category(self):
                c = self.create_category()
                c1 = self.create_category_other()
                p = self.create_product(category=c)
                p1 = self.create_product_other(category=c1)
                self.assertTrue(isinstance(c, Category))
                self.assertTrue(isinstance(c1, Category))
                self.assertTrue(isinstance(p, Product))
                self.assertTrue(isinstance(p1, Product))
                response = self.client.get(reverse('shop:product_list_by_category', args=[c.slug]))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context['category'], c)
                self.assertQuerysetEqual(response.context['categories'], ['<Category: exportaciones>', '<Category: exportaciones_uno>'])
                self.assertQuerysetEqual(response.context['products'], ['<Product: exportaciones_bolivia>'])


class ProductDetailTest(TestCase):

        def create_category(self, name="exportaciones", slug="exportaciones-colombia"):
                return Category.objects.create(name=name, slug=slug)

        def create_product(self, category="", name="exportaciones_bolivia", slug="exportaciones-bolivia", description="exportaciones a Bolivia", available="True", created=datetime.now(), updated=datetime.now()):
                return Product.objects.create(category=category, name=name, slug=slug, description=description, available=available, created=created, updated=updated)

        def test_product_detail(self):
                c = self.create_category()
                p = self.create_product(category=c)
                self.assertTrue(isinstance(c, Category))
                self.assertTrue(isinstance(p, Product))
                response = self.client.get(reverse('shop:product_detail', args=[p.id, 'exportaciones-bolivia']))
                print response
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context['product'], p)
                print response.context['cart_product_form']
                self.assertTrue(response.context['cart_product_form'].is_valid())
