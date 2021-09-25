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
		selected_fields = kwargs.pop('selected_fields', None)
		'''if selected_fields is None:
			pass
			#selected_fields=self.selected_fields
		else:
			print(self.Meta.model._meta.verbose_name,"+++++++++++++++++++++++++",selected_fields)
			print("-->",selected_fields)'''
		#got my hooks into the fields' data.
		#now have to push it back into an object for serialization, but only when requested
		# Instantiate the superclass normally
		super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
		
		
		
		if selected_fields is not None:
			#print(self)
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(selected_fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)
			#self.selected_fields=list(allowed)


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






class VoyageDatesSerializer(DynamicFieldsModelSerializer):
	'''arrival_year=serializers.SerializerMethodField('get_arrival_year')
	def get_arrival_year(self,obj):
		#print(obj)
		return obj.get_date_year(obj.imp_arrival_at_port_of_dis)'''
	
	'''#def to_representation(self, instance):
	def __init__(self,d):
		print(self.parent.selected_fields)
		#self.selected_fields
		print("why not")
		#print(self.parent.selected_fields)
		#self.selected_fields=self.parent.selected_fields
		#print(self.selected_fields)'''
	
		
	class Meta:
		model=VoyageDates
		exclude=('id','voyage')
	



'''
#This is the closest they DRF folks seem to have come to what we really need here: https://github.com/encode/django-rest-framework/issues/1985
class VoyageDatePKField(serializers.PrimaryKeyRelatedField):
	def get_queryset(self):
		voyage_dates__imp_length_home_to_disembark=self.context['request'].voyage_dates__imp_length_home_to_disembark
		queryset = Voyage.objects.filter(voyage_dates__imp_length_home_to_disembark__)
'''




class VoyageSerializer(DynamicFieldsModelSerializer):
	
	
	##I need to find a way to pass the fields into these nested serializers, to be able to filter sub-fields
	###This is the closest they DRF folks seem to have come to it: https://github.com/encode/django-rest-framework/issues/1985
	###So it does demand a custom solution.
	###This document, then, will be the base mode, in which we present the long-form data and allow you to search on all of it.
	#####After that, I can make custom serializer classes that focus in on particular facets of the data.
	#####For instance, stats-oriented serializer classes that quickly analyze the numerical data, or names, or geographical regions.
	###But, ideally, it would be possible to nest serializers and pass them a list of fields to dynamically restrict the display of, in the way that one can filter a queryset with a keyword argument.
	##In the meantime, we can at least filter on the categories...
	#voyage_dates=serializers.ListField(read_only=True, child=VoyageDatesSerializer())
	#kw_args=SerializerMethodField()
	#kw_args.get_value(self,'selected_fields')
	voyage_dates=VoyageDatesSerializer()
	#voyage_dates=SerializerMethodField()
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
		
	'''def get_kw_args(self,d):
		def __init__(self,d):
			print(self.selected_fields)
		return ['voyage_dates']'''
	
	def get_queryset(self):
		queryset.prefetch_related("voyage_dates__imp_length_home_to_disembark")
		queryset.prefetch_related("voyage_dates__imp_length_leaving_africa_to_disembark")
		return queryset
	
	'''def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print('TOP LEVEL CONTEXT',kwargs)
		# We pass the "upper serializer" context to the "nested one"
		self.fields['voyage_dates'].context.update(kwargs)'''
	
	'''def get_voyage_dates(self,obj):
		return VoyageDatesSerializer(obj.VoyageDates.all(), many=True, selected_fields=self.selected_fields).data'''
	