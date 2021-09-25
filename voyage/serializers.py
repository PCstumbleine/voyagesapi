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
		super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
		
		if selected_fields is not None:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(selected_fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)


##### GEO ##### 

class RegionSerializer(serializers.ModelSerializer):
	
	
	class Meta:
		model=Region
		fields=('__all__')

class PlaceSerializer(serializers.ModelSerializer):
	class Meta:
		model=Place
		fields=('__all__')

##### NUMBERS ##### 

class VoyageSlavesNumbersSerializer(serializers.ModelSerializer):
	def __init__(self):
		print(self.get_fields)
	
	class Meta:
		model=VoyageSlavesNumbers
		fields=('__all__')

##### VESSEL VARIABLES ##### 
###at first glance, i seem only to be getting values on three of the below.

class VoyageShipSerializer(serializers.ModelSerializer):
	rig_of_vessel=serializers.SlugRelatedField(slug_field='label',read_only='True')
	imputed_nationality=serializers.SlugRelatedField(slug_field='label',read_only='True')
	nationality_ship=serializers.SlugRelatedField(slug_field='label',read_only='True')
	ton_type=serializers.SlugRelatedField(slug_field='label',read_only='True')
	vessel_construction_place=serializers.SlugRelatedField(slug_field='label',read_only='True')
	vessel_construction_region=serializers.SlugRelatedField(slug_field='label',read_only='True')
	registered_place=serializers.SlugRelatedField(slug_field='label',read_only='True')
	registered_region=serializers.SlugRelatedField(slug_field='label',read_only='True')
	class Meta:
		model=VoyageShip
		exclude=('id','voyage')

##### DATES, NUMBERS, ITINERARY ##### 

class VoyageSlavesNumbersSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		exclude=('id','voyage')

class VoyageItinerarySerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		exclude=('id','voyage')

##### OUTCOMES #####

class VoyageOutcomeSerializer(serializers.ModelSerializer):
	outcome_owner=serializers.SlugRelatedField(slug_field='label',read_only='True')
	outcome_slaves=serializers.SlugRelatedField(slug_field='label',read_only='True')
	particular_outcome=serializers.SlugRelatedField(slug_field='label',read_only='True')
	resistance=serializers.SlugRelatedField(slug_field='label',read_only='True')
	vessel_captured_outcome=serializers.SlugRelatedField(slug_field='label',read_only='True')
	class Meta:
		model=VoyageOutcome
		exclude=('id','voyage')
		
##### GROUPINGS ##### 

class VoyageGroupingsSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageGroupings
		fields=('__all__')

##### CREW, CAPTAIN, OWNER ##### 

class VoyageCrewSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageCrew
		exclude=('id','voyage')

class VoyageCaptainSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageCaptain
		exclude=('id',)

class VoyageShipOwnerSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageShipOwner
		fields=('name',)

##### SOURCES ##### 

class VoyageSourcesSerializer(serializers.ModelSerializer):
	source_type=serializers.SlugRelatedField(slug_field='group_name',read_only='True')
	class Meta:
		model=VoyageSources
		fields=('full_ref','source_type')

class VoyageDatesSerializer(DynamicFieldsModelSerializer):
	arrival_year=serializers.SerializerMethodField('get_arrival_year')
	def get_arrival_year(self,obj):
		#print(obj)
		return obj.get_date_year(obj.imp_arrival_at_port_of_dis)
		
	class Meta:
		model=VoyageDates
		exclude=('id','voyage')

class VoyageSerializer(DynamicFieldsModelSerializer):
	
	voyage_dates=VoyageDatesSerializer()
	voyage_ship=VoyageShipSerializer()
	voyage_groupings=serializers.SlugRelatedField(slug_field='label',read_only='True')
	voyage_crew=VoyageCrewSerializer()
	voyage_sources=VoyageSourcesSerializer(many=True,read_only=True)
	voyage_captain=VoyageCaptainSerializer(many=True,read_only=True)
	voyage_ship_owner=VoyageShipOwnerSerializer(many=True,read_only=True)
	voyage_slaves_numbers=VoyageSlavesNumbersSerializer()
	voyage_itinerary=VoyageItinerarySerializer()
	voyage_outcomes=VoyageOutcomeSerializer(many=True,read_only=True)	
	
	 
	class Meta:
		model=Voyage
		fields='__all__'