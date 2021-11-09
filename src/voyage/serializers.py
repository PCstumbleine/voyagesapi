from rest_framework import serializers
from rest_framework.fields import SerializerMethodField,IntegerField,CharField
import re
from .models import *

#https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
#https://www.django-rest-framework.org/api-guide/serializers/#build_standard_fieldself-field_name-model_field

def onestepdown(selected_fields):
	fields_dict={i.split('__')[0]:[] for i in selected_fields}
	for s in selected_fields:
		prefix=s.split('__')[0]
		if len(prefix)<len(s):
			suffix=s[len(prefix)+2:]
			fields_dict[prefix].append(suffix)
	return fields_dict

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		selected_fields = kwargs.pop('selected_fields', None)
		super().__init__(*args, **kwargs)
		if selected_fields is not None:
			fields_dict=onestepdown(selected_fields)
			allowed=set(fields_dict.keys())
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

##### GEO #####


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

##### VESSEL VARIABLES ##### 

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
	rig_of_vessel=RigOfVesselSerializer(many=False)
	imputed_nationality=NationalitySerializer(many=False)
	ton_type=TonTypeSerializer(many=False)
	vessel_construction_place=PlaceSerializer(many=False)
	vessel_construction_region=RegionSerializer(many=False)
	registered_place=PlaceSerializer(many=False)
	registered_region=RegionSerializer(many=False)
	
	class Meta:
		model=VoyageShip
		fields='__all__'

##### NUMBERS ##### 

class VoyageSlavesNumbersSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields='__all__'




##### ITINERARY #####

class VoyageItinerarySerializer(DynamicFieldsModelSerializer):
	imp_broad_region_voyage_begin=BroadRegionSerializer(many=False)	
	port_of_departure=PlaceSerializer(many=False)
	int_first_port_emb=PlaceSerializer(many=False)
	int_second_port_emb=PlaceSerializer(many=False)
	int_first_region_purchase_slaves=RegionSerializer(many=False)
	int_second_region_purchase_slaves=RegionSerializer(many=False)
	int_first_port_dis=PlaceSerializer(many=False)
	int_second_port_dis=PlaceSerializer(many=False)
	int_first_region_slave_landing=RegionSerializer(many=False)
	imp_principal_region_slave_dis=RegionSerializer(many=False)
	int_second_place_region_slave_landing=RegionSerializer(many=False)
	first_place_slave_purchase=PlaceSerializer(many=False)
	second_place_slave_purchase=PlaceSerializer(many=False)
	third_place_slave_purchase=PlaceSerializer(many=False)
	first_region_slave_emb=RegionSerializer(many=False)
	second_region_slave_emb=RegionSerializer(many=False)
	third_region_slave_emb=RegionSerializer(many=False)
	port_of_call_before_atl_crossing=PlaceSerializer(many=False)
	first_landing_place=PlaceSerializer(many=False)
	second_landing_place=PlaceSerializer(many=False)
	third_landing_place=PlaceSerializer(many=False)
	first_landing_region=RegionSerializer(many=False)
	second_landing_region=RegionSerializer(many=False)
	third_landing_region=RegionSerializer(many=False)
	place_voyage_ended=PlaceSerializer(many=False)
	region_of_return=RegionSerializer(many=False)
	broad_region_of_return=BroadRegionSerializer(many=False)
	imp_port_voyage_begin=PlaceSerializer(many=False)
	imp_region_voyage_begin=RegionSerializer(many=False)
	imp_broad_region_voyage_begin=BroadRegionSerializer(many=False)
	principal_place_of_slave_purchase=PlaceSerializer(many=False)
	imp_principal_place_of_slave_purchase=PlaceSerializer(many=False)
	imp_principal_region_of_slave_purchase=RegionSerializer(many=False)
	imp_broad_region_of_slave_purchase=BroadRegionSerializer(many=False)
	principal_port_of_slave_dis=PlaceSerializer(many=False)
	imp_principal_port_slave_dis=PlaceSerializer(many=False)
	imp_broad_region_slave_dis=BroadRegionSerializer(many=False)
	class Meta:
		model=VoyageItinerary
		fields='__all__'

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
	outcome_owner=OwnerOutcomeSerializer(many=False)
	outcome_slaves=SlavesOutcomeSerializer(many=False)
	particular_outcome=ParticularOutcomeSerializer(many=False)
	resistance=ResistanceSerializer(many=False)
	vessel_captured_outcome=VesselCapturedOutcomeSerializer(many=False)
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
		
	voyage_itinerary=VoyageItinerarySerializer(many=False)
	voyage_dates=VoyageDatesSerializer(many=False)
	voyage_dates=VoyageDatesSerializer(many=False)
	voyage_groupings=VoyageGroupingsSerializer(many=False)
	voyage_crew=VoyageCrewSerializer(many=False)
	voyage_sources=VoyageSourcesSerializer(many=True,read_only=True)
	voyage_ship=VoyageShipSerializer(many=False)
	voyage_captain=VoyageCaptainSerializer(many=True,read_only=True)
	voyage_ship_owner=VoyageShipOwnerSerializer(many=True,read_only=True)
	voyage_slaves_numbers=VoyageSlavesNumbersSerializer(many=False)
	voyage_outcomes=VoyageOutcomeSerializer(many=True,read_only=True)
	class Meta:
		model=Voyage
		fields='__all__'
