from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

class InputFile(models.Model):
    name = models.CharField(max_length=300, verbose_name="File name")
    url = models.CharField(max_length=500, verbose_name="URL or location of the file")
    from_date = models.DateField(auto_now=False, verbose_name="Starting date in file")
    to_date = models.DateField(auto_now=False, verbose_name="Finishing date in file")
    filesize = models.IntegerField(verbose_name="File Size")
    is_public = models.BooleanField(verbose_name="Should the file be public")

    def __str__(self):
        return "%s - %s" %(self.name, self.url)

class InputFileForm(ModelForm):
    class Meta:
        model = InputFile
        fields = ['name','url','from_date','to_date','filesize','is_public']


