import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
sys.path.append('/datos/Kiosco/ku-master/source/')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

