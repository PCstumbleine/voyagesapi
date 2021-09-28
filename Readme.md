
## Voyages REST API

This is an attempt to rebuild the Voyages API with as few dependencies as possible in the latest versions of django and python

To launch the project
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt


The app has one working endpoint, but it's quite flexible.

http://127.0.0.1:8000/voyage/

* schema endpoint: OPTIONS http call to 127.0.0.1:8000/voyage/
	* my code here is not ideal, but the below documentation simply didn't work
		* http://www.tomchristie.com/rest-framework-2-docs/topics/documenting-your-api#endpoint-documentation
		* https://www.django-rest-framework.org/api-guide/generic-views/#retrievemodelmixin
	* in the meantime, I return a nested dictionary with:
		* serializer var names as keys
			* which can be concatenated with a double underscore "__" for a fully-qualified var name
			* and therefore passed back as search terms or display filters			
		* labels for display to the user, taken from the model (via the serializer)
		* string representations of data types, which can be used to construct the appropriate search interface

* parameters (on GET http calls):
	* "selected_fields": accepts any top-level variable, e.g. 
		* "voyage_ship"
		* "voyage_crew"
		* (in other words, table names in our sql schema)
	* "results_per_page": number of results. accepts an integer
	* "results_page": the page number. accepts an integer
* filter vars:
	* any fully-qualified varible
	* performs two kinds of search:
		* min/max on a comma-separated range for numerical values
		* inexact contains (sql "iLike") for text fields
	* one special filter: "voyage_ids": accepts comma-separated integers

For instance, try out: http://127.0.0.1:8000/voyage/?selected_fields=voyage_ship,voyage_ship_owner&voyage_ship_owner__name=Domingos Pacheco

Next steps:
1. Provide selection helper endpoints
	1. min & max for numeric types, in order to be able to auto-populate slider scales
	1. distinct values for selection fields (e.g. the geo variables)
1. Create an interface that uses the above to display human-readable labels for interactive variables (so a searchable table is the basic form of this)
1. Begin to refine views by focusing in on subsets of the data (like numerical data, or names, or geographic regions)

I've also included some db migration scripts (clear.sh does it all if the hard-coded variables are correct).
