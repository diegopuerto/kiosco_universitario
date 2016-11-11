from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from models import InputFile, InputFileForm, List, File_List
from extras import save_uploaded_file, create_zip

def insert_file(request, file_id=1):
    if request.method =='POST':
        print("request.post: %s"%request.POST)
        print("request.files: %s"%request.FILES)
        print("file_id: %s"%file_id)
       
        if 'id_modify' in request.POST:
            instance = get_object_or_404(InputFile, id=file_id)
            input_file_form = InputFileForm(request.POST or None, instance=instance)
            if input_file_form.is_valid():
                message = "Form is valid"
                print(message)
                input_file = input_file_form.save()
            pending_input_files = InputFile.objects.filter(data_pending=True)
            return render(request,'file_server/pending_files.html',{'message':message, 'pending_input_files':pending_input_files})
        else:
            for input_file in request.FILES:
                filename = request.FILES[input_file].name
                print ("filename: %s"%filename)
                input_file_path = save_uploaded_file(request.FILES[input_file],filename)
                print ("input_file_path: %s"%input_file_path)
                filesize = 345
                data = {
                    'name':filename,
                    'filesize':filesize,
                    'url':input_file_path,
                    'data_pending':True,
                }
                input_file_form = InputFileForm(data)
                print("input_file_form: %s"%input_file_form)
                message = "Insertion not successfull"
                if input_file_form.is_valid():
                    input_file = input_file_form.save()
                    message = "File stored in DB: %s"%input_file
                    print(message)

            return HttpResponse("Coronamos")

    else: # GET
        if file_id:
            try:
                input_file = InputFile.objects.get(pk=file_id)
            except:
                return HttpResponse('El archivo con referencia %s no existe' % file_id)
            input_file_form = InputFileForm(instance=input_file)
            print(input_file_form)
            return render(request,'file_server/modify_file.html',{'input_file_form':input_file_form, 'file_id':file_id})
        else:
            input_file_form = InputFileForm()
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
    print("request.post: %s"%request.POST)
    print("request.files: %s"%request.FILES)
    query_list = []
    for item in request.POST:
        print ("item :%s"%item)
        if 'file_' in item:
            print("req_value %s"%request.POST[item])
            query_list.append(int(item.split("file_")[1]))
    print ("query_list: %s"%query_list)
    file_list = InputFile.objects.filter(pk__in=query_list)
    print ("file_list: %s"%file_list)
#    for inputfile in query_list:
#        a = File_List.objects.filter(inputfile__in=query_list[inputfile])
    is_created = create_zip(file_list)
    
#    is_created=True
    if not is_created:
        return HttpResponse("mal: %s"%file_list)
    else:
        return HttpResponse("bien: %s"%is_created)



