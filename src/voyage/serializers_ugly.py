from rest_framework import serializers
from rest_framework.fields import SerializerMethodField,IntegerField,CharField
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

#this allows for field selection on a nested basis.
#it should be folded in with the dynamic fields model serializer above
#like, seriously. this is rather hodgepodge...
#labels are now governed by the end destination so that is going to have to be fixed through some kind of inheritance. working on it.
def field_select(serializer,selected_fieldnames,tableserializers):
	print(selected_fieldnames)
	if selected_fieldnames != None:
		selected_fields={}
		for s in selected_fieldnames:
			table=s.split('__')[0]
			field=s[len(table)+2:]
			if table not in selected_fields:
				selected_fields[table]=[field]
			else:
				selected_fields[table].append(field)
		selected_tables=[t for t in selected_fields if selected_fields[t]!=['']]
		for tablename in selected_tables:
			t=tableserializers[tablename]
			#len 2 means it comes with parameters, like read_only=True,many=True
			#len 1 means no parameters
			if len(t)==2:
				serializercall="%s(%s,selected_fields=['%s'])" %(t[0],t[1],'\',\''.join(selected_fields[tablename]))
			elif len(t)==1:
				serializercall="%s(selected_fields=['%s'])" %(t[0],'\',\''.join(selected_fields[tablename]))
			serializer.fields[tablename]=eval(serializercall)
			#this next line passes the kwargs down to the next nested serializer
			serializer.fields[tablename].context.update(serializer.context)
		selected_nontable_fields=[t for t in selected_fields if selected_fields[t]==['']]
		serializerfields=list(serializer.fields)
		
		for f in serializerfields:
			if f not in selected_fields:
				del(serializer.fields[f])
		
		'''for f in serializer.fields:
			print(f,serializer.fields[f],serializer.fields[f].context)'''
		
	else:
		
		for tablename in tableserializers:
			t=tableserializers[tablename]
			if len(t)==2:
				serializercall="%s(%s)" %(t[0],t[1])
			elif len(t)==1:
				serializercall="%s()" %(t[0])
			serializer.fields[tablename]=eval(serializercall)
	return serializer

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

class NationalitySerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Nationality
		fields='__all__'

class TonTypeSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=TonType
		fields='__all__'

class VoyageShipSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageShip
		fields='__all__'
	def __init__(self, *args, **kwargs):
		selected_fieldnames = kwargs.pop('selected_fields', None)
		super(VoyageShipSerializer, self).__init__(*args, **kwargs)
		tableserializers={
		'rig_of_vessel':['RigOfVesselSerializer'],
		'imputed_nationality':['NationalitySerializer'],
		'nationality_ship':['NationalitySerializer'],
		'ton_type':['TonTypeSerializer'],
		'vessel_construction_place':['PlaceSerializer'],
		'vessel_construction_region':['RegionSerializer'],
		'registered_place':['PlaceSerializer'],
		'registered_region':['RegionSerializer']
		}
		self=field_select(self,selected_fieldnames,tableserializers)

##### DATES, NUMBERS, ITINERARY ##### 

class VoyageSlavesNumbersSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields='__all__'



class PlaceSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Place
		fields='__all__'

class RegionSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=Region
		fields='__all__'

class BroadRegionSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=BroadRegion
		fields='__all__'


class VoyageItinerarySerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageItinerary
		fields='__all__'
	def __init__(self, *args, **kwargs):
		selected_fieldnames = kwargs.pop('selected_fields', None)
		
		super(VoyageItinerarySerializer, self).__init__(*args, **kwargs)
		tableserializers={
			'port_of_departure':['PlaceSerializer','read_only=True,many=False'],
			'int_first_port_emb':['PlaceSerializer','read_only=True,many=False'],
			'int_second_port_emb':['PlaceSerializer','read_only=True,many=False'],
			'int_first_region_purchase_slaves':['RegionSerializer','read_only=True,many=False'],
			'int_second_region_purchase_slaves':['RegionSerializer','read_only=True,many=False'],
			'int_first_port_dis':['PlaceSerializer','read_only=True,many=False'],
			'int_second_port_dis':['PlaceSerializer','read_only=True,many=False'],
			'int_first_region_slave_landing':['RegionSerializer','read_only=True,many=False'],
			'int_second_place_region_slave_landing':['PlaceSerializer','read_only=True,many=False'],
			'first_place_slave_purchase':['PlaceSerializer','read_only=True,many=False'],
			'second_place_slave_purchase':['PlaceSerializer','read_only=True,many=False'],
			'third_place_slave_purchase':['PlaceSerializer','read_only=True,many=False'],
			'first_region_slave_emb':['RegionSerializer','read_only=True,many=False'],
			'second_region_slave_emb':['RegionSerializer','read_only=True,many=False'],
			'third_region_slave_emb':['RegionSerializer','read_only=True,many=False'],
			'port_of_call_before_atl_crossing':['PlaceSerializer','read_only=True,many=False'],
			'first_landing_place':['PlaceSerializer','read_only=True,many=False'],
			'second_landing_place':['PlaceSerializer','read_only=True,many=False'],
			'third_landing_place':['PlaceSerializer','read_only=True,many=False'],
			'first_landing_region':['RegionSerializer','read_only=True,many=False'],
			'second_landing_region':['RegionSerializer','read_only=True,many=False'],
			'third_landing_region':['RegionSerializer','read_only=True,many=False'],
			'place_voyage_ended':['PlaceSerializer','read_only=True,many=False'],
			'region_of_return':['RegionSerializer','read_only=True,many=False'],
			'broad_region_of_return':['BroadRegionSerializer','read_only=True,many=False'],
			'imp_port_voyage_begin':['PlaceSerializer','read_only=True,many=False'],
			'imp_region_voyage_begin':['RegionSerializer','read_only=True,many=False'],
			'imp_broad_region_voyage_begin':['BroadRegionSerializer','read_only=True,many=False'],
			'principal_place_of_slave_purchase':['PlaceSerializer','read_only=True,many=False'],
			'imp_principal_place_of_slave_purchase':['PlaceSerializer','read_only=True,many=False'],
			'imp_principal_region_of_slave_purchase':['RegionSerializer','read_only=True,many=False'],
			'imp_broad_region_of_slave_purchase':['BroadRegionSerializer','read_only=True,many=False'],
			'principal_port_of_slave_dis':['PlaceSerializer','read_only=True,many=False'],
			'imp_principal_port_slave_dis':['PlaceSerializer','read_only=True,many=False'],
			'imp_principal_region_slave_dis':['RegionSerializer','read_only=True,many=False'],
			'imp_broad_region_slave_dis':['BroadRegionSerializer','read_only=True,many=False']
		}
		
		self=field_select(self,selected_fieldnames,tableserializers)

##### SOURCES ##### 


class VoyageSourcesSerializer(DynamicFieldsModelSerializer):
	#source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=VoyageSources
		fields='__all__'
		
##### OUTCOMES #####


class ParticularOutcomeSerializer(DynamicFieldsModelSerializer):
	#source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=ParticularOutcome
		fields='__all__'


class SlavesOutcomeSerializer(DynamicFieldsModelSerializer):
	#source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=SlavesOutcome
		fields='__all__'
		
class ResistanceSerializer(DynamicFieldsModelSerializer):
	#source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=Resistance
		fields='__all__'

class OwnerOutcomeSerializer(DynamicFieldsModelSerializer):
	#source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=OwnerOutcome
		fields='__all__'

class VesselCapturedOutcomeSerializer(DynamicFieldsModelSerializer):
	#source_type=serializers.SlugRelatedField(default=CharField,slug_field='group_name',read_only=True)
	class Meta:
		model=VesselCapturedOutcome
		fields='__all__'
		
class VoyageOutcomeSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageOutcome
		fields='__all__'
	def __init__(self, *args, **kwargs):
		selected_fieldnames = kwargs.pop('selected_fields', None)
		super(VoyageOutcomeSerializer, self).__init__(*args, **kwargs)
		tableserializers={
			'outcome_owner':['RigOfVesselSerializer','read_only=True,many=False'],
			'outcome_slaves':['NationalitySerializer','read_only=True,many=False'],
			'particular_outcome':['NationalitySerializer','read_only=True,many=False'],
			'resistance':['TonTypeSerializer','read_only=True,many=False'],
			'vessel_captured_outcome':['VesselCapturedOutcomeSerializer','read_only=True,many=False']
		}
		self=field_select(self,selected_fieldnames,tableserializers)

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

class VoyageSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=Voyage
		fields='__all__'
	def __init__(self, *args, **kwargs):
		selected_fieldnames = kwargs.pop('selected_fields', None)
		super(VoyageSerializer, self).__init__(*args, **kwargs)
		tableserializers={
			"voyage_dates":["VoyageDatesSerializer","many=False"],
			"voyage_groupings":["VoyageGroupingsSerializer"],
			"voyage_crew":["VoyageCrewSerializer"],
			"voyage_sources":["VoyageSourcesSerializer","many=True,read_only=True"],
			"voyage_ship":["VoyageShipSerializer"],
			"voyage_captain":["VoyageCaptainSerializer","many=True,read_only=True"],
			"voyage_ship_owner":["VoyageShipOwnerSerializer","many=True,read_only=True"],
			"voyage_slaves_numbers":["VoyageSlavesNumbersSerializer"],
			"voyage_itinerary":["VoyageItinerarySerializer","many=False"],
			"voyage_outcomes":["VoyageOutcomeSerializer","many=True,read_only=True"]
		}
		self=field_select(self,selected_fieldnames,tableserializers)


#"voyage_itinerary":["VoyageItinerarySerializer","excluded_fields=('id','voyage')"],
