
## Voyages REST API, 2021

This is an attempt to rebuild the Voyages API with as few dependencies as possible in the latest versions of django and python

To launch the project

	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt

## 2 GET endpoints

Both allow you to:

* filter the queryset on any variable value
	* text fields using sql inexact case insensitive: 
	* numeric fields using ranges [lower,upper] (lower can == upper)
	* e.g. voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812
* select only specific columns to return, e.g., selected_fields=voyage_dates__imp_arrival_at_port_of_dis_year,voyage_slaves_numbers__imp_total_num_slaves_disembarked
* try to get an autocomplete endpoint in place for certain fields

next up:

* consider table-level sorting so I don't have to name every single variable
* consider (though maybe the above would sort this well enough) alternate endpoints (places, ships...)
* start folding in geojson data

### Paginated, tabular-style endpoint: GET http call to 127.0.0.1:8000/voyage/

* Intended to reproduce the Voyages data table with a default of 10 per page
* but now with nested data (it returns long-form serialized json)!
* Pagination args:
	* "results_per_page": number of results. accepts an integer
	* "results_page": the page number. accepts an integer
* one special filter: "voyage_ids": accepts comma-separated integers

For instance, try

	GET http://127.0.0.1:8000/voyage/?voyage_ship_owner__name=Domingos%20Pacheco&selected_fields=voyage_ship_owner__name
	GET http://127.0.0.1:8000/voyage/?selected_fields=voyage_dates__imp_arrival_at_port_of_dis_year,voyage_slaves_numbers__imp_total_num_slaves_disembarked&voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812

next up:

* better pagination (at the very least, a total results datapoint)
* sort_by functionality
* better text searching?
	* integrate [domingos' in-memory levenstein fuzzy match](https://github.com/rice-crc/voyages/blob/09acf9dafc721044198a6172e4d3e3b3f9132379/voyages/apps/past/models.py#L45)

### DataFrame-style endpoint: GET http call to 127.0.0.1:8000/voyage/dataframes/

* Intended to grab all results in selected columns as arrays for client-side faceted interactivity
* Not super fast, but it's usable as of Oct. 19. Built in parallel with https://github.com/JohnMulligan/voyagesapi_plotly

For instance, try

	GET http://127.0.0.1:8000/voyage/dataframes?voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812&selected_fields=voyage_dates__imp_arrival_at_port_of_dis_year,voyage_slaves_numbers__imp_total_num_slaves_disembarked

next up:

* benchmark performance
* experiment performance with
	* complex searches
	* better-tailored dataframe selection (the data-heavy graphs are impressive for their interactivity but it is slow)
	* alternatively, creative ways of adding to dataframes, like fetching one year at a time and updating the graph as you go....
* experiment with caching

## OPTIONS endpoint: OPTIONS http call to 127.0.0.1:8000/voyage/

Only one argument: hierarchical=True -- default is flat.

Otherwise, it simply returns, straight from the django models:

* the fully-qualified variable names
	* which can be used for
		* filtering by values on a get call, e.g. voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812
		* selecting columns on a get call, e.g. selected_fields=voyage_dates__imp_arrival_at_port_of_dis_year,voyage_slaves_numbers__imp_total_num_slaves_disembarked
	* and whose components can be identified in django style with double underscores
* their data types (so far just numeric and text)
* their labels
	* for consumption by the end-user
	* these are taken, again straight from the model, live -- which means vars' display labels can be rewritten simply by changing that parameter for that variable in models.py

Its utility inheres in providing programmers the ability to very quickly build readable interfaces into the data.

next up:

* if i build my own autocomplete, flag the fields that's available for
* consider adding a min/max field (or extra arg or endpoint to retrieve it) on numeric fields, to allow for easy building of slider interface elements by devs

## Notes

1. Obvs, you'll need a .sql dump. Contact me.
	1. I'm using a purupose-built one.
	1. Less data in it (voyages only)
	1. Rendered a few fields numeric (dates that were string fields)
1. My code here is not ideal, but the below documentation simply didn't yield good results. 
	1. Why I wrote my own options endpoint:
		1. http://www.tomchristie.com/rest-framework-2-docs/topics/documenting-your-api#endpoint-documentation
		1. https://www.django-rest-framework.org/api-guide/generic-views/#retrievemodelmixin
	1. Why I wrote my own column selection function:
		1. This doesn't do everything it could: #https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
1. I've also included some db migration scripts
	1. don't bother, they're not well-written
	1. clear.sh does it all if the hard-coded variables are correct (they're not)
