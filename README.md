The Web application is up and running ([link](https://gtgonline-parinporecha.rhcloud.com/))

If you want to check out the UI of GTGOnline!, you can use the following credentials -
 * email - test@test.com
 * pass - testtest

or you can view the screenshots ([here](http://imgur.com/a/NOKse#0))

If you want to run this application on your own server, here's how you can -

**Requirements - SQL server, Django >= 1.4 (1.5 is preferable)**

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
- Run the script `install.sh`(`./install.sh`). It will create all the tables needed, and the log directories and logfiles.
- Run ```python manage.py runserver```. It will start a server at ```localhost:8000```. You can specify other address and port no. by running ```python manage.py runserver <<ADDRESS>>:<<PORT NO.>>```
- Thats it !
- If you face any other errors, please contact the developer

I've written a sync backend for Getting Things Gnome! which syncs tasks with GTGOnline!
It uses REST API and the documentation can be found [here](http://gtgonline-parinporecha.rhcloud.com/api/api_docs/)

For bug reporting, please open an issue or contact the developer
