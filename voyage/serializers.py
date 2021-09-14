from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *

#Use this to layer in the reader-friendly table labels
class SerialLabeler(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		super(SerialLabeler, self).__init__(*args, **kwargs)
		self.fields['labels'] = SerializerMethodField()
	def get_labels(self, *args):
		try:
			labels = {
				'verbose_name':self.Meta.model._meta.verbose_name,
				'verbose_name_plural':self.Meta.model._meta.verbose_name_plural}
			return labels
		except:
			pass





##### GEO DATA ##### 

class RegionSerializer(SerialLabeler):
	class Meta:
		model=Region
		fields='__all__'

class PlaceSerializer(SerialLabeler):
	class Meta:
		model=Place
		fields='__all__'





##### VESSEL VARIABLES DOWNSTREAM OF VOYAGE_SHIP ##### 
		
class RigTypeSerializer(SerialLabeler):
	class Meta:
		model=RigOfVessel
		fields='__all__'

class TonTypeSerializer(SerialLabeler):
	class Meta:
		model=TonType
		fields='__all__'

class NationalitySerializer(SerialLabeler):
	class Meta:
		model=Nationality
		fields='__all__'

class VoyageShipSerializer(SerialLabeler):
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
	def get_labels(self, *args):
		print(self.Meta.model._meta.get_field('ton_type').verbose_name)



##### DATES ##### 

class VoyageDatesSerializer(SerialLabeler):
	arrival_year=serializers.SerializerMethodField('get_arrival_year')
	def get_arrival_year(self,d):
		return d.get_date_year(d.imp_arrival_at_port_of_dis)
	
	class Meta:
		model=VoyageDates
		fields = '__all__'
		
##### GROUPINGS ##### 

class VoyageGroupingsSerializer(SerialLabeler):
	class Meta:
		model=VoyageGroupings
		fields=('__all__')


##### CREW ##### 

class VoyageCrewSerializer(SerialLabeler):
	class Meta:
		model=VoyageCrew
		fields=('__all__')

class VoyageSerializer(SerialLabeler):
	#id = serializers.Field()
	voyage_dates=VoyageDatesSerializer()
	voyage_ship=VoyageShipSerializer()
	voyage_groupings=VoyageGroupingsSerializer()
	voyage_crew=VoyageCrewSerializer()
	class Meta:
		model=Voyage
		
		fields=(
			'voyage_id',
			'voyage_dates',
			'voyage_ship',
			'voyage_groupings',
			'voyage_crew'
			)