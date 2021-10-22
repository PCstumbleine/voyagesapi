This folder contains some brute scripts for shifting chunks of the voyages db over

I found it necessary because of
* how touchy django migrations can be
* the double-bind foreign key weirdness that voyages has going on
* other such crud :)