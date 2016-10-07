from django.shortcuts import render
from django.http import HttpResponse

from models import InputFile, InputFileForm

def insert_file(request, file_id=1):
    if request.method =='POST':
        print(request.POST)
        print(request.FILES)
        input_file_form = InputFileForm(request.POST)
#        print(input_file_form)
        if input_file_form.is_valid():
            input_file = input_file_form.save()
#            print(input_file)
        return HttpResponse("Almacenado con exito")
    else:
        if file_id:
            try:
                input_file = InputFile.objects.get(pk=file_id)
            except:
                return HttpResponse('El archivo con referencia %s no existe' % file_id)
            input_file_form = InputFileForm(instance=input_file)
            print(input_file_form)
            return render(request,'file_server/input_file.html',{'input_file_form':input_file_form})
        else:
            input_file_form = InputFileForm()
            print(input_file_form)
            return render(request,'file_server/input_file.html',{'input_file_form':input_file_form})

