from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

class InputFile(models.Model):
    name = models.CharField(max_length=300, verbose_name="File name")
    url = models.CharField(max_length=500, verbose_name="URL or location of the file")
    from_date = models.DateField(auto_now=False, verbose_name="Starting date in file", blank=True, null=True)
    to_date = models.DateField(auto_now=False, verbose_name="Finishing date in file", blank=True, null=True)
    filesize = models.IntegerField(verbose_name="File Size")
    is_public = models.BooleanField(verbose_name="Should the file be public?", default=False)
    data_pending = models.BooleanField(verbose_name="Is there any pending data in the file?", default=True)

    def __str__(self):
        return "%s" %(self.name)

class List(models.Model):
    name = models.CharField(max_length=64, verbose_name="List of files")
    download_path = models.CharField(max_length=300, verbose_name="Path to the compressed zip file containing the files")

    def __str__(self):
        return "%s" %self.name

    def list_size(self):
        return "%s" %(File_List.objects.filter(listname=self.name).count())

class File_List(models.Model):
    inputfile = models.ForeignKey('InputFile', verbose_name="File that belongs to the list")
    listname = models.ForeignKey('List', verbose_name="Name of the list containing the file")
    creation_date = models.DateTimeField(auto_now=True)
    remaining_downloads = models.IntegerField()


    def __str__(self):
        return "%s: %s" %(self.inputfile, self.listname)


class InputFileForm(ModelForm):
    class Meta:
        model = InputFile
        fields = ['name','url','from_date','to_date','filesize','is_public','data_pending']


