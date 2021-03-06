# Proyect Summary

## Project structure:

- source	
	- apps
	- base
    - libs
	- templates
	- media  
	- static
	- db.sqlite
	- manage.py
	- docs
	- readme.md
	
### Folders explanation
**source:** Contains all the source code for the project.

**apps:** Contains the apps used in the project

**base:** Contains the settings files for the manage of the apps in the wholle project

**libs:** Contains source code which does not belong to Django itself (I.E. develops that are not apps) but are used in the project

**templates:** Contains the most generic templates used all along the project (like headers and footers)

**media:** Contains the media files (like audio and image files) which are uploaded by the front end (by admins or users)

**static:** Static files (like css, js, even audio and image files) which are used and setted from the back end

### Installation

$ virtualenv -p python2.7 venv      # This installs python2.7 as the main interpreter, required for successful pip install
$ pip install -r requirements.txt

### Testing

$ source venv/bin/activate
$ cd source
$ python manage.py migrate
$ python manage.py fix_permissions
$ python manage.py initialdata
$ python manage.py runserver 0.0.0.0:8000  # No errors sholud be presented

Open a local browser and go to 127.0.0.1:8000, you should see Kiosco's main page
