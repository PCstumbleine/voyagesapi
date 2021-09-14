
## Voyages REST API

This is an attempt to rebuild the Voyages API with as few dependencies as possible in the latest versions of django and python

To launch the project
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt

Then it gets tricky: you'll want a db with only the voyages_ tables for the time being. Once you have that, you can more or less run the manual_db_migrations scripts (clear.sh does it all if the hard-coded variables are correct).

The app has two working endpoints, and most of the voyages variables are mapped.

1. Minimum number of captives disembarked: http://127.0.0.1:8000/voyage/min_number_disembarked/N?format=json
1. Voyage by id: http://127.0.0.1:8000/voyage/by_id/N

It seems pretty fast -- this is encouraging.

Next steps:
1. Make use of verbose var names
	1. pivot the fields mis-labeled as "label" into a "value"
	1. tag those with their labels
1. Doing the above should do a lot to clean up the json, though it will mean more bandwidth is being consumed. benchmark this?
1. Try to make some generalized endpoint methods
	1. numerical filters
	1. text fields (start with django's iLike then get Domingos to implement his in-mem levenstein fuzzy search)
	1. geo filters? django now has geojson methods which could be quite powerful for user interfaces
