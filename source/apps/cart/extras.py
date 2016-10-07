from shop.models import Product
import zipfile
from datetime import datetime

try:
    import zlib
    zipmode = zipfile.ZIP_DEFLATED
except:
    zipmode = zipfile.ZIP_STORED

def get_and_compress(csv_files):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    raw_files = Product.objects.filter(id__in=csv_files)
    filename = timestamp+'.zip'
    with zipfile.ZipFile(filename,'a',zipmode) as compressed_file:
        for raw_file in raw_files:
            compressed_file.write(raw_file)

        

