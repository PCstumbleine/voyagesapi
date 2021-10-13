from rest_framework import serializers
from rest_framework.fields import SerializerMethodField,IntegerField,CharField
import re
from .models import *
from .data_viz import *


#https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
	"""
	A ModelSerializer that takes an additional `fields` argument that
	controls which fields should be displayed.
	"""
	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		#help(self)
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


class VoyageShipSerializer(DynamicFieldsModelSerializer):
	rig_of_vessel=serializers.SlugRelatedField(slug_field='label',read_only=True)
	imputed_nationality=serializers.SlugRelatedField(slug_field='label',read_only=True)
	nationality_ship=serializers.SlugRelatedField(slug_field='label',read_only=True)
	ton_type=serializers.SlugRelatedField(slug_field='label',read_only=True)
	vessel_construction_place=serializers.SlugRelatedField(slug_field='place',read_only=True)
	vessel_construction_region=serializers.SlugRelatedField(slug_field='region',read_only=True)
	registered_place=serializers.SlugRelatedField(slug_field='place',read_only=True)
	registered_region=serializers.SlugRelatedField(slug_field='region',read_only=True)
	class Meta:
		model=VoyageShip
		fields='__all__'

##### DATES, NUMBERS, ITINERARY ##### 

class VoyageSlavesNumbersSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields='__all__'

class VoyageItinerarySerializer(DynamicFieldsModelSerializer):
	port_of_departure = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	int_first_port_emb = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	int_second_port_emb = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	int_first_region_purchase_slaves = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	int_second_region_purchase_slaves = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	int_first_port_dis = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	int_second_port_dis = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	int_first_region_slave_landing = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	int_second_place_region_slave_landing = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	first_place_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	second_place_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	third_place_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	first_region_slave_emb = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	second_region_slave_emb = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	third_region_slave_emb = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	port_of_call_before_atl_crossing = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	first_landing_place = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	second_landing_place = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	third_landing_place = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	first_landing_region = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	second_landing_region = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	third_landing_region = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	place_voyage_ended = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	region_of_return = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	broad_region_of_return = serializers.SlugRelatedField(default=CharField,slug_field='broad_region',read_only=True)
	imp_port_voyage_begin = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	imp_region_voyage_begin = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	imp_broad_region_voyage_begin = serializers.SlugRelatedField(default=CharField,slug_field='broad_region',read_only=True)
	principal_place_of_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	imp_principal_place_of_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	imp_principal_region_of_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	imp_broad_region_of_slave_purchase = serializers.SlugRelatedField(default=CharField,slug_field='broad_region',read_only=True)
	principal_port_of_slave_dis = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	imp_principal_port_slave_dis = serializers.SlugRelatedField(default=CharField,slug_field='place',read_only=True)
	imp_principal_region_slave_dis = serializers.SlugRelatedField(default=CharField,slug_field='region',read_only=True)
	imp_broad_region_slave_dis = serializers.SlugRelatedField(default=CharField,slug_field='broad_region',read_only=True)
	class Meta:
		model=VoyageItinerary
		fields='__all__'
	class Meta:
		model=VoyageItinerary
		fields='__all__'

##### SOURCES ##### 


class VoyageSourcesSerializer(DynamicFieldsModelSerializer):
	source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=VoyageSources
		fields='__all__'
		
##### OUTCOMES #####

class VoyageOutcomeSerializer(DynamicFieldsModelSerializer):
	outcome_owner=serializers.SlugRelatedField(default=CharField,slug_field='label',read_only=True)
	outcome_slaves=serializers.SlugRelatedField(default=CharField,slug_field='label',read_only=True)
	particular_outcome=serializers.SlugRelatedField(default=CharField,slug_field='label',read_only=True)
	resistance=serializers.SlugRelatedField(default=CharField,slug_field='label',read_only=True)
	vessel_captured_outcome=serializers.SlugRelatedField(default=CharField,slug_field='label',read_only=True)
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

class VoyageDatesSerializer(DynamicFieldsModelSerializer):
	#the serializermethodfield types return a default field of "<class 'rest_framework.fields.empty'>"
	#so I decided to park that with the appropriate rest framework datatype (here, IntegerField)
	#my view looks to __dict__['default'] for the type when it encounters a SerializerMethodField
	class Meta:
		model=VoyageDates
		fields='__all__'

class VoyageSerializer(DynamicFieldsModelSerializer):
	
	class Meta:
		model=Voyage
		fields='__all__'
	def __init__(self, *args, **kwargs):
		super(VoyageSerializer, self).__init__(*args, **kwargs)
		selected_fieldnames = kwargs.pop('selected_fields', None)
		
		tabledict={
			"voyage_dates":["VoyageDatesSerializer","excluded_fields=('id','voyage')"],
			"voyage_groupings":["VoyageGroupingsSerializer","selected_fields=('label',)"],
			"voyage_crew":["VoyageCrewSerializer","excluded_fields=('id','voyage')"],
			"voyage_sources":["VoyageSourcesSerializer","many=True,read_only=True"],
			"voyage_itinerary":["VoyageItinerarySerializer","excluded_fields=('id','voyage')"],
			"voyage_ship":["VoyageShipSerializer","excluded_fields=('id','voyage')"],
			"voyage_captain":["VoyageCaptainSerializer","excluded_fields=('id','voyage'),many=True,read_only=True"],
			"voyage_ship_owner":["VoyageShipOwnerSerializer","excluded_fields=('id','voyage'),many=True,read_only=True"],
			"voyage_slaves_numbers":["VoyageSlavesNumbersSerializer","excluded_fields=('id','voyage')"],
			"voyage_outcomes":["VoyageOutcomeSerializer","many=True,read_only=True,excluded_fields=('id','voyage')"]
		}
		
		print('+++++++++',selected_fieldnames)
		if selected_fieldnames==['voyage_id']:
			print('----->voyageidonly')
			self.fields='voyage_id'
		elif selected_fieldnames != None:
			selected_fields={}
			for s in selected_fieldnames:
				table,field=s.split('__')
				if table not in selected_fields:
					selected_fields[table]=[field]
				else:
					selected_fields[table].append(field)
			for tablename in selected_fields:
				serializercall="%s(%s,selected_fields=['%s'])" %(tabledict[tablename][0],tabledict[tablename][1],'\',\''.join(selected_fields[tablename]))
				print(serializercall)
				self.fields[tablename]=eval(serializercall)
		else:
			for table in tabledict:
				serializercall="%s(%s)" %(tabledict[table][0],tabledict[table][1])
				self.fields[table]=eval(serializercall)