from datetime import datetime
from os import chown
from zipfile import ZipFile
from hashlib import md5
from datetime import datetime

FILE_PATH = '/datos/Kiosco/'

def save_uploaded_file(f,nombre):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = FILE_PATH+nombre+'_'+timestamp
    with open(filename,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        chown(filename,14,50)
    except Exception as e:
        print ("No se pudo cambiar permisos: %s"%e)
        
    return filename

def create_zip(file_list):
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    md5().update(stamp.encode('utf-8'))
    name = md5().hexdigest()
    try:
        for input_file in file_list:
            with ZipFile(name+'.zip', mode='w') as zf:
                zf.write(input_file.url)
        return True
    except Exception as e:
        print (e)
        return False


