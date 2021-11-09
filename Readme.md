# Voyages REST API 2021

This is an attempt to rebuild the Voyages API with as few dependencies as possible in the latest versions of django and python

## Local Deployment

Create an external Docker network.

```bash
host:~/Projects/voyagesapi$ docker network create voyagesapi
```

Build and run the containers.

```bash
host:~/Projects/voyagesapi$ docker-compose up -d --build
```

Create the database.

```bash
host:~/Projects/voyagesapi$ docker exec -i voyagesapi-mysql mysql -uroot -pvoyages -e "create database voyages"
```

Import the database dump to MySQL.

```bash
host:~/Projects/voyagesapi$ docker exec -i voyagesapi-mysql mysql -uroot -pvoyages voyages < data/voyagesapi.sql
```

View container logs.

```bash
host:~/Projects/voyagesapi$ docker logs voyagesapi-django
host:~/Projects/voyagesapi$ docker logs voyagesapi-mysql
```

*The Adminer app is provided as an additional way to work with the database.*

Note the following project resources:

* Voyages API: http://127.0.0.1:8000/
* Adminer: http://127.0.0.1:8080

## Cleanup

```bash
host:~/Projects/voyagesapi$ docker-compose down

host:~/Projects/voyagesapi$ docker container prune
host:~/Projects/voyagesapi$ docker image prune
host:~/Projects/voyagesapi$ docker volume prune
host:~/Projects/voyagesapi$ docker network prune
```

## API Endpoints

The two current endpoints allow you to:

* filter the queryset on any variable value
	* text fields using sql inexact case insensitive:
	* numeric fields using ranges [lower,upper] (lower can == upper)
	* e.g. voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812
* select only specific columns to return, e.g., selected_fields=voyage_dates__imp_arrival_at_port_of_dis_year,voyage_slaves_numbers__imp_total_num_slaves_disembarked

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

```
GET http://127.0.0.1:8000/voyage/?selected_fields=voyage_ship,voyage_ship_owner&voyage_ship_owner__name=Domingos%20Pacheco
```

next up:

* better pagination (at the very least, a total results datapoint)
* sort_by functionality
* better text searching?
	* integrate [domingos' in-memory levenstein fuzzy match](https://github.com/rice-crc/voyages/blob/09acf9dafc721044198a6172e4d3e3b3f9132379/voyages/apps/past/models.py#L45)

### DataFrame-style endpoint: GET http call to 127.0.0.1:8000/voyage/dataframes/

* Intended to grab all results in selected columns as arrays for client-side faceted interactivity
* Not super fast, but it's usable as of Oct. 19. Built in parallel with https://github.com/JohnMulligan/voyagesapi_plotly

For instance, try

```
GET http://127.0.0.1:8000/voyage/dataframes?voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812
```

### OPTIONS endpoint: OPTIONS http call to 127.0.0.1:8000/voyage/

simply returns

* the fully-qualified variable names
	* which can be used for
		* filtering by values on a get call, e.g. voyage_dates__imp_arrival_at_port_of_dis_year=1810,1812
		* selecting columns on a get call, e.g. selected_fields=voyage_dates__imp_arrival_at_port_of_dis_year,voyage_slaves_numbers__imp_total_num_slaves_disembarked
	* and whose components can be identified in django style with double underscores
* their data types (so far just numeric and text)
* their labels
	* for consumption by the end-user
	* no longer taken directly from the models due to labeling issues on related fields

next up:

* if i build my own autocomplete, flag the fields that's available for
* consider adding a min/max field (or extra arg or endpoint to retrieve it) on numeric fields, to allow for easy building of slider interface elements by devs

## Notes

1. SQL changes
	1. Less data in it (voyages only)
	1. Rendered a few fields numeric (dates that were string fields)
1. Dynamic serializer field selection code from https://stackoverflow.com/a/58505856
1. I've also included some db migration scripts
	1. don't bother, they're not well-written
	1. clear.sh does it all if the hard-coded variables are correct (they're not)
