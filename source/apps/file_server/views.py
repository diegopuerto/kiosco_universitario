from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from models import InputFile, InputFileForm
from extras import save_uploaded_file, create_zip

import logging

#Create loggers
logger = logging.getLogger(__name__)

def insert_file(request, file_id=1):
    if request.method =='POST':
        logger.debug("request.post: %s"%request.POST)
        logger.debug("request.files: %s"%request.FILES)
        logger.debug("file_id: %s"%file_id)
       
        if 'id_modify' in request.POST:
            instance = get_object_or_404(InputFile, id=file_id)
            input_file_form = InputFileForm(request.POST or None, instance=instance)
            if input_file_form.is_valid():
                message = "Form is valid"
                logger.debug(message)
                print(message)
                input_file = input_file_form.save()
            pending_input_files = InputFile.objects.filter(data_pending=True)
            return render(request,'file_server/pending_files.html',{'message':message, 'pending_input_files':pending_input_files})
        else:
            for input_file in request.FILES:
                filename = request.FILES[input_file].name
                logger.debug("filename: %s"%filename)
                print ("filename: %s"%filename)
                input_file_path = save_uploaded_file(request.FILES[input_file],filename)
                logger.debug("input_file_path: %s"%input_file_path)
                print ("input_file_path: %s"%input_file_path)
                filesize = 345
                data = {
                    'name':filename,
                    'filesize':filesize,
                    'url':input_file_path,
                    'data_pending':True,
                }
                input_file_form = InputFileForm(data)
                logger.debug("input_file_form: %s"%input_file_form)
                print("input_file_form: %s"%input_file_form)
                message = "Insertion not successfull"
                if input_file_form.is_valid():
                    input_file = input_file_form.save()
                    message = "File stored in DB: %s"%input_file
                    logger.debug(message)
                    print(message)

            return HttpResponse("Coronamos")

    else: # GET
        if file_id:
            try:
                input_file = InputFile.objects.get(pk=file_id)
            except:
                return HttpResponse('El archivo con referencia %s no existe' % file_id)
            input_file_form = InputFileForm(instance=input_file)
            logger.debug(input_file_form)
            print(input_file_form)
            return render(request,'file_server/modify_file.html',{'input_file_form':input_file_form, 'file_id':file_id})
        else:
            input_file_form = InputFileForm()
            logger.debug(input_file_form)
            print(input_file_form)
            return render(request,'file_server/input_file.html',{'input_file_form':input_file_form})

def pending_files(request):
    message = "Hola"
    pending_input_files = InputFile.objects.filter(data_pending=True)
    return render(request,'file_server/pending_files.html',{'message':message, 'pending_input_files':pending_input_files})

def public_file_list(request):
    message = "Hola"
    public_files = InputFile.objects.filter(is_public=True)
    return render(request,'file_server/public_files.html',{'message':message, 'public_files':public_files})

def all_files_list(request):
    message = "Hola"
    all_files = InputFile.objects.all()
    return render(request,'file_server/all_files.html',{'message':message, 'all_files':all_files})

def checkout(request):
    logger.debug("request.post: %s"%request.POST)
    logger.debug("request.files: %s"%request.FILES)
    print("request.post: %s"%request.POST)
    print("request.files: %s"%request.FILES)
    query_list = []
    for item in request.POST:
        logger.debug("item :%s"%item)
        print ("item :%s"%item)
        if 'file_' in item:
            logger.debug("req_value %s"%request.POST[item])
            print("req_value %s"%request.POST[item])
            query_list.append(int(item.split("file_")[1]))
    file_list = InputFile.objects.filter(pk__in=query_list)
    logger.debug(file_list)
    print (file_list)
    if create_zip(file_list):
        return HttpResponse("bien: %s"%file_list)
    else:
        return HttpResponse("mal: %s"%file_list)
