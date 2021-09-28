from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import re
from .models import *


#https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
	"""
	A ModelSerializer that takes an additional `fields` argument that
	controls which fields should be displayed.
	"""

	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		selected_fields = kwargs.pop('selected_fields', None)
		excluded_fields=kwargs.pop('excluded_fields',None)
		super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
		
		if selected_fields is not None:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(selected_fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)
		if excluded_fields is not None:
			disallowed=set(excluded_fields)
			existing=set(self.fields)
			for field_name in existing.intersection(disallowed):
				self.fields.pop(field_name)

##### GEO ##### 

class RegionSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Region
		fields='__all__'

class PlaceSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Place
		fields='__all__'
	
class NationalitySerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Nationality
		fields='__all__'


##### NUMBERS ##### 

class VoyageSlavesNumbersSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields='__all__'

##### VESSEL VARIABLES ##### 
###at first glance, i seem only to be getting values on three of the below.

class RigOfVesselSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=RigOfVessel
		fields='__all__'
		
class TonTypeSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=TonType
		fields='__all__'
		
class VoyageShipSerializer(DynamicFieldsModelSerializer):
	rig_of_vessel=RigOfVesselSerializer(selected_fields=('label',))
	imputed_nationality=NationalitySerializer(selected_fields=('label',))
	nationality_ship=NationalitySerializer(selected_fields=('label',))
	ton_type=TonTypeSerializer(selected_fields=('label',))
	vessel_construction_place=PlaceSerializer(selected_fields=('label',))
	vessel_construction_region=RegionSerializer(selected_fields=('label',))
	registered_place=PlaceSerializer(selected_fields=('label',))
	registered_region=RegionSerializer(selected_fields=('label',))
	class Meta:
		model=VoyageShip
		fields='__all__'

##### DATES, NUMBERS, ITINERARY ##### 

class VoyageSlavesNumbersSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields='__all__'

class VoyageItinerarySerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields='__all__'

##### OUTCOMES #####

class OwnerOutcomeSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=OwnerOutcome
		fields='__all__'

class SlavesOutcomeSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=SlavesOutcome
		fields='__all__'

class ParticularOutcomeSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=ParticularOutcome
		fields='__all__'

class ResistanceSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Resistance
		fields='__all__'

class VesselCapturedOutcomeSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VesselCapturedOutcome
		fields='__all__'

class VoyageOutcomeSerializer(DynamicFieldsModelSerializer):
	outcome_owner=OwnerOutcomeSerializer()
	outcome_slaves=SlavesOutcomeSerializer()
	particular_outcome=ParticularOutcomeSerializer()
	resistance=ResistanceSerializer()
	vessel_captured_outcome=VesselCapturedOutcomeSerializer()
	class Meta:
		model=VoyageOutcome
		fields='__all__'
		
##### GROUPINGS ##### 

class VoyageGroupingsSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageGroupings
		fields='__all__'

##### CREW, CAPTAIN, OWNER ##### 

class VoyageCrewSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageCrew
		fields='__all__'

class VoyageCaptainSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageCaptain
		fields='__all__'

class VoyageShipOwnerSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageShipOwner
		fields='__all__'

##### SOURCES ##### 


class VoyageSourcesSerializer(serializers.ModelSerializer):
	source_type = serializers.SlugRelatedField(slug_field='group_name',read_only=True)
	class Meta:
		model=VoyageSources
		fields=('full_ref','source_type')

class VoyageDatesSerializer(DynamicFieldsModelSerializer):
	arrival_year=serializers.SerializerMethodField('get_arrival_year')
	def get_arrival_year(self,obj):
		return obj.get_date_year(obj.imp_arrival_at_port_of_dis)
	class Meta:
		model=VoyageDates
		fields='__all__'

class VoyageSerializer(DynamicFieldsModelSerializer):
	
	voyage_dates=VoyageDatesSerializer(excluded_fields=('id','voyage'))
	voyage_ship=VoyageShipSerializer(excluded_fields=('id','voyage'))
	voyage_groupings=VoyageGroupingsSerializer(selected_fields=('label',))
	voyage_crew=VoyageCrewSerializer(excluded_fields=('id','voyage'))
	voyage_sources=VoyageSourcesSerializer(many=True,read_only=True)
	voyage_captain=VoyageCaptainSerializer(excluded_fields=('id','voyage'),many=True,read_only=True)
	voyage_ship_owner=VoyageShipOwnerSerializer(excluded_fields=('id','voyage'),many=True,read_only=True)
	voyage_slaves_numbers=VoyageSlavesNumbersSerializer(excluded_fields=('id','voyage'))
	voyage_itinerary=VoyageItinerarySerializer(excluded_fields=('id','voyage'))
	voyage_outcomes=VoyageOutcomeSerializer(excluded_fields=('id','voyage'),read_only=True)
	 
	class Meta:
		model=Voyage
		fields='__all__'