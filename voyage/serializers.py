from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *

'''#Use this to layer in the reader-friendly table labels
class serializers.ModelSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		super(serializers.ModelSerializer, self).__init__(*args, **kwargs)
		self.fields['labels'] = SerializerMethodField()
	def get_labels(self, *args):
		try:
			labels = {
				'verbose_name':self.Meta.model._meta.verbose_name,
				'verbose_name_plural':self.Meta.model._meta.verbose_name_plural}
			return labels
		except:
			pass
'''




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
	class Meta:
		model=VoyageSlavesNumbers
		fields=('__all__')







##### VESSEL VARIABLES DOWNSTREAM OF VOYAGE_SHIP ##### 
		
class RigTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model=RigOfVessel
		fields=('__all__')
		
class TonTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model=TonType
		fields=('__all__')

class NationalitySerializer(serializers.ModelSerializer):
	class Meta:
		model=Nationality
		fields=('__all__')

class VoyageShipSerializer(serializers.ModelSerializer):
	nationality_ship=NationalitySerializer()
	imputed_nationality=NationalitySerializer()
	ton_type=TonTypeSerializer()
	rig_of_vessel=RigTypeSerializer()
	vessel_construction_place=PlaceSerializer()
	vessel_construction_region=RegionSerializer()
	registered_place=PlaceSerializer()
	registered_region=RegionSerializer()
	class Meta:
		model=VoyageShip
		fields=('__all__')



##### DATES, NUMBERS, ITINERARY ##### 

class VoyageDatesSerializer(serializers.ModelSerializer):
	arrival_year=serializers.SerializerMethodField('get_arrival_year')
	def get_arrival_year(self,d):
		return d.get_date_year(d.imp_arrival_at_port_of_dis)
	
	class Meta:
		model=VoyageDates
		fields = ('__all__')

class VoyageSlavesNumbersSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields = ('__all__')

class VoyageItinerarySerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageSlavesNumbers
		fields = ('__all__')







##### OUTCOMES #####


class VesselCapturedOutcomeSerializer(serializers.ModelSerializer):
	class Meta:
		model=VesselCapturedOutcome
		fields=('__all__')
class OwnerOutcomeSerializer(serializers.ModelSerializer):
	class Meta:
		model=OwnerOutcome
		fields=('__all__')
class SlavesOutcomeSerializer(serializers.ModelSerializer):
	class Meta:
		model=SlavesOutcome
		fields=('__all__')
class ParticularOutcomeSerializer(serializers.ModelSerializer):
	class Meta:
		model=ParticularOutcome
		fields=('__all__')
class ResistanceSerializer(serializers.ModelSerializer):
	class Meta:
		model=Resistance
		fields=('__all__')

class VoyageOutcomeSerializer(serializers.ModelSerializer):
	outcome_owner=OwnerOutcomeSerializer()
	outcome_slaves=SlavesOutcomeSerializer()
	particular_outcome=ParticularOutcomeSerializer()
	resistance=ResistanceSerializer()
	vessel_captured_outcome=VesselCapturedOutcomeSerializer()
	class Meta:
		model=VoyageOutcome
		fields=('__all__')





		
##### GROUPINGS ##### 

class VoyageGroupingsSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageGroupings
		fields=('__all__')


##### CREW, CAPTAIN, OWNER ##### 

class VoyageCrewSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageCrew
		fields=('__all__')

class VoyageCaptainSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageCaptain
		fields=('__all__')

class VoyageShipOwnerSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageShipOwner
		fields=('__all__')


##### SOURCES ##### 

class VoyageSourcesTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model=VoyageSourcesType
		fields=('__all__')

class VoyageSourcesSerializer(serializers.ModelSerializer):
	source_type=VoyageSourcesTypeSerializer()
	class Meta:
		model=VoyageSources
		fields=('__all__')


class VoyageSerializer(serializers.ModelSerializer):
	#id = serializers.Field()
	voyage_dates=VoyageDatesSerializer()
	voyage_ship=VoyageShipSerializer()
	voyage_groupings=VoyageGroupingsSerializer()
	voyage_crew=VoyageCrewSerializer()
	voyage_sources=VoyageSourcesSerializer(many=True,read_only=True)
	voyage_captain=VoyageCaptainSerializer(many=True,read_only=True)
	voyage_ship_owner=VoyageShipOwnerSerializer(many=True,read_only=True)
	voyage_slaves_numbers=VoyageSlavesNumbersSerializer()
	voyage_itinerary=VoyageItinerarySerializer()
	voyage_outcomes=VoyageOutcomeSerializer(many=True,read_only=True)
	class Meta:
		model=Voyage
		fields=('__all__')



	

