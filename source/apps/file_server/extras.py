from datetime import datetime
from os import chown
from zipfile import ZipFile
from hashlib import md5
from datetime import datetime

#FILE_PATH = '/datos/Kiosco/'                        ## Directorio sysweb03
FILE_PATH = '/home/juan/work/dane/datos/Kiosco/'    ## Directorio lenny

def save_uploaded_file(f,nombre):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = FILE_PATH+timestamp+'_'+nombre
    with open(filename,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        chown(filename,14,50)
    except Exception as e:
        print ("No se pudo cambiar permisos: %s"%e)
        
    return filename

def create_zip(name,file_list):
#    stamp = ''
#    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
#    print ("stamp: %s"%stamp)
#    hash1 = md5(stamp.encode('utf-8'))
#    name = FILE_PATH+hash1.hexdigest()
#    print ("name: %s"%name)
    try:
        for input_file in file_list:
            with ZipFile(name+'.zip', mode='w') as zf:
                zf.write(input_file.url)
        return name+'.zip'
    except Exception as e:
        print ("Error: %s"%e)
        return False

