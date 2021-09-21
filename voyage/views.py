from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import json
from .models import Voyage
from .serializers import VoyageSerializer

#def index(request):
#    return HttpResponse("Hello, world. You're at the voyages index.")

defaultlimit=10

'''class VoyageSourcesConnectionByID(APIView):

	def get(self,request,id):
	
		#this is just a test -- presupposing only a voyage id column
		if id:
			try:
				queryset=VoyageSourcesConnection.objects.get(id=id)
			except VoyageSourcesConnection.DoesNotExist:
				return Response({'error': 'voyage source connection does not exist'},status=400)
			read_serializer = VoyageSourcesConnectionSerializer(queryset)
		
		else:		
			queryset=VoyageSourcesConnection.objects.all().values()
			read_serializer=VoyageSourcesConnectionSerializer(queryset,many=True)

		return Response(read_serializer.data)'''


class VoyageByID(APIView):

	def get(self,request,id):
	
		#this is just a test -- presupposing only a voyage id column
		if id:
			try:
				queryset=Voyage.objects.get(voyage_id=id)
			except Voyage.DoesNotExist:
				return Response({'error': 'voyage does not exist'},status=400)
			read_serializer = VoyageSerializer(queryset)
		
		else:		
			queryset=Voyage.objects.all().values()
			read_serializer=VoyageSerializer(queryset,many=True)

		return Response(read_serializer.data)

class VoyageByMinDisembarked(APIView):
	
	def get(self,request,imp_total_num_slaves_disembarked):
	
		queryset=Voyage.objects.filter(voyage_slaves_numbers__imp_total_num_slaves_disembarked__gt=imp_total_num_slaves_disembarked)
		
		read_serializer = VoyageSerializer(queryset,many=True)
		
		return Response(read_serializer.data)
	

class VoyageByMinDisembarked(APIView):
	
	def get(self,request,imp_total_num_slaves_disembarked):
	
		queryset=Voyage.objects.filter(voyage_slaves_numbers__imp_total_num_slaves_disembarked__gt=imp_total_num_slaves_disembarked)
		
		read_serializer = VoyageSerializer(queryset,many=True)
		
		return Response(read_serializer.data)

#lookups: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups
#and stacking query vars: https://docs.djangoproject.com/en/3.2/topics/db/queries/#querysets-are-lazy

class VoyageList(APIView):
	
	#serializer_class=VoyageSerializer
	
	
	
	def get(self,request):
		#the base queryset contains all voyages
		queryset=Voyage.objects.all()
		
		#we're going to have a reserved field via which calls can request only basic 
		
		
		
		#now we just have to enumerate our varibles and build filters for them.
		voyage_ids=self.request.query_params.get('voyage_ids')
		
		if voyage_ids!=None:
			voyage_id=[i for i in voyage_ids.split(',')]
			queryset = queryset.filter(voyage_id__in=voyage_id)
		
		read_serializer=VoyageSerializer(queryset,many=True,fields=('voyage_id',))
		
		return Response(read_serializer.data)
		



'''class VoyageView(APIView):
	
	def get(self,request):
		query_params=request.query_params
		if query_params=={}:
			queryset=Voyage.objects.all()
			serializer=VoyageSerializer(queryset[:defaultlimit],many=True)
		else:
			print("PARAMS------------")
			#https://docs.djangoproject.com/en/3.2/ref/models/querysets/#icontains
			print(query_params)
			queryset=Voyage.objects.all().values()
			read_serializer=VoyageSerializer(queryset[0])
			
		return JsonResponse(serializer.data, safe=False)'''
		
