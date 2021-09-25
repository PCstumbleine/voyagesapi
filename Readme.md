
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
1. Make a schema of nested, serialized variables' metadata available as an endpoint
1. Present long-form data, fully searchable, with basic nested serializers
1. Create an interface that uses both to display human-readable labels for interactive variables (so a searchable table is the basic form of this)
1. Begin to refine views by focusing in on subsets of the data (like numerical data, or names, or geographic regions)