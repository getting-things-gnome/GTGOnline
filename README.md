The Web application is up and running ([link](https://gtgonline-parinporecha.rhcloud.com/))

If you want to run this application on your own server, here's how you can -

Requirements - SQL server, Django >= 1.4 (1.5 is preferable)

- Create a database. For MySQL it is - `CREATE DATABASE <<NAME OF THE DATABASE YOU WANT>> CHARACTER SET utf8 COLLATE utf8_general_ci;` (If you are using PostgreSQL or SQLite, make sure that the character set is UTF-8)

Open the file `GTGOnline/settings.py`, and replace the lines 42 to 51 -

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # database backend
    		'NAME': 'demo', # name of the database
    		'USER': 'parin', # user other than root
    		'PASSWORD': 'parin',
    		'HOST': '',
    		'PORT': ''
    	}
    }
with your configuration.
- Run ```python manage.py syncdb```. It will create all the tables needed and ask you for your credentials.
- Run ```python manage.py runserver```. It will start a server at ```localhost:8000```. You can specify other port nos. by running ```python manage.py runserver <<PORT NO.>>```
- Thats it !
- If you face any other errors, please contact the developer

I've written a sync backend for Getting Things Gnome! which syncs tasks with GTGOnline!
It uses REST API and the documentation can be found [here](http://gtgonline-parinporecha.rhcloud.com/api/api_docs/)

For bug reporting, please open an issue or contact the developer
