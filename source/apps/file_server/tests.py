from django.test import TestCase
from datetime import datetime
from .models import InputFile 

class InputFileTest(TestCase):

        def create_InputFile(self, name="exportacione_cuba", url="/home/cualquier_carpeta", from_date=datetime.now(), to_date=datetime.now(), filesize=24, is_public=True, data_pending=False ):
                return InputFile.objects.create(name=name, url=url, from_date=from_date, to_date=to_date, filesize=filesize, is_public=is_public, data_pending=data_pending)

        def test_create_category(self):
                i = self.create_InputFile()
                self.assertTrue(isinstance(i, InputFile))
                self.assertEqual(i.__str__(), "%s - %s" %(i.name, i.url))
