
## Voyages REST API

This is an attempt to rebuild the Voyages API from scratch in the latest versions of django and python

In doing so, at the least I'm determining which variables are functionally necessary and which are not, and seeing how fast it will run without solr.

Sept. 13: The database structure is such a pain.
* The 2-way FK constraints mean the serializer picks up lots of unnecessary data. is it a huge concern? No. But it's messy.
* The date fields aren't being logged as datetimes or years but as comma-separated text fields that allow for nulls -- this despite the fact that the user can see, for instance "imputed year of arrival with slaves." easy to do on sql but would require an update to the impute fields. could the model do the parsing so it returns this year and thus can be sorted on?



To launch the project
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate

You'll then need to have the Voyages db set up on an accessible mysql db
Set your connections in a file named dbcheckconf.json (example provided)
Create an empty database with the appropriate name
You can then run `python db_shift.py` to migrate the tables I've already worked through from production to the working app

Kick off the dev app with `python manage.py runserver`

Only one endpoint just now: 127.0.0.1:8000/voyages/VOYAGEID



installation got weird for me on the sql client side...
(venv) jcm10@C02V41K9HV2Q voyages_gallery_to_omeka % export LDFLAGS="-L/usr/local/lib -L/usr/local/opt/openssl/lib" 
(venv) jcm10@C02V41K9HV2Q voyages_gallery_to_omeka % export CPPFLAGS="-I/usr/local/include -I/usr/local/opt/openssl/include" 
