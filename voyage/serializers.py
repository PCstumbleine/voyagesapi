from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import re
from .models import *










##We want a means of extracting out of every field
###name
###label
###type
####if numeric:
####min_value
####max_value
####if not, some placeholder search function until we can plug in domingos' levenstein search cache for text fields

###VoyageSerializer.Meta.model._meta.verbose_name
###VoyageSerializer.Meta.model.get_deferred_fields
###VoyageSerializer.Meta.model.get_fields





#https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
	"""
	A ModelSerializer that takes an additional `fields` argument that
	controls which fields should be displayed.
	"""

	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		fields = kwargs.pop('fields', None)
		
		'''#got my hooks into the fields' data.
		#now have to push it back into an object for serialization, but only when requested
		for f in self.fields:
			print(f,self.fields[f].label)
			try:
				for sf in self.fields[f]:
					#print(sf.__dict__)
					print('+',sf.name,'+',sf.label,'+',sf._field)
			except:
				pass'''

		# Instantiate the superclass normally
		super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
		
		print(fields)
		if fields is not None:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)


##### GEO DATA ##### 

class RegionSerializer(serializers.ModelSerializer):
	
	
	class Meta:
		model=Region
		fields=('__all__')

class PlaceSerializer(serializers.ModelSerializer):
	class Meta:
		model=Place
		fields=('__all__')






##### NUMBERS DATA ##### 

class VoyageSlavesNumbersSerializer(serializers.ModelSerializer):
	def __init__(self):
		print(self.get_fields)
	
	class Meta:
		model=VoyageSlavesNumbers
		fields=('__all__')







##### VESSEL VARIABLES DOWNSTREAM OF VOYAGE_SHIP ##### 

class VoyageShipSerializer(serializers.ModelSerializer):
	rig_of_vessel=serializers.SlugRelatedField(slug_field='label',read_only='True')
	imputed_nationality=serializers.SlugRelatedField(slug_field='label',read_only='True')
	'''nationality_ship=NationalitySerializer()
	imputed_nationality=NationalitySerializer()
	ton_type=TonTypeSerializer()
	rig_of_vessel=RigTypeSerializer()
	vessel_construction_place=PlaceSerializer()
	vessel_construction_region=RegionSerializer()
	registered_place=PlaceSerializer()
	registered_region=RegionSerializer()'''
	class Meta:
		model=VoyageShip
		exclude=('id','voyage')


##### DATES, NUMBERS, ITINERARY ##### 

class VoyageDatesSerializer(serializers.ModelSerializer):
	arrival_year=serializers.SerializerMethodField('get_arrival_year')
	def get_arrival_year(self,d):
		return d.get_date_year(d.imp_arrival_at_port_of_dis)
	
	class Meta:
		model=VoyageDates
		exclude=('id','voyage')

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


#This would be an interesting way of doing it -- presenting each entity in a simple "value"/"label" pair
#Would allow for totally ignorant apps to hit this thing and present it in a readable way
#But it's less data-heavy to give a flatter representation instead, I think, so I'm going for the slugs
'''class VoyageShipOwnerSerializer(serializers.ModelSerializer):
	value=serializers.SerializerMethodField()
	label=serializers.SerializerMethodField()
	class Meta:
		model=VoyageShipOwner
		fields=('value','label',)
	def get_value(self,instance):
		return instance.name
	def get_label(self,instance):
		return self.Meta.model._meta.verbose_name'''


##### SOURCES ##### 

class VoyageSourcesSerializer(serializers.ModelSerializer):
	source_type=serializers.SlugRelatedField(slug_field='group_name',read_only='True')
	class Meta:
		model=VoyageSources
		fields=('full_ref','source_type')


class VoyageSerializer(DynamicFieldsModelSerializer):
	#id = serializers.Field()
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


	



