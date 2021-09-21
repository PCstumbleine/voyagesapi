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


#lookups: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups

class VoyageByMinDisembarked(APIView):
	
	def get(self,request,imp_total_num_slaves_disembarked):
	
		queryset=Voyage.objects.filter(voyage_slaves_numbers__imp_total_num_slaves_disembarked__gt=imp_total_num_slaves_disembarked)
		
		read_serializer = VoyageSerializer(queryset,many=True)
		
		return Response(read_serializer.data)
	






class VoyageList(APIView):
	
	def get(self,request):

		params=self.request.query_params
		
		
		#FIELD SELECTION
		## selected_fields
		### this is important because responses can quickly become large enough (not on the SQL side but on spitting them back out) to dramatically slow the response time
		default_query_fields='__all__'
		selected_fields=params.get('selected_query_fields')
		if selected_fields!=None:
			selected_query_fields=(i for i in selected_fields.split(','))
		else:
			selected_query_fields=default_query_fields
		
		#now we just have to enumerate our varibles and build filters for them.
		voyage_ids=params.get('voyage_ids')
		
		
		#PAGINATION
		## results_per_page
		## results_page
		default_results_per_page=10
		default_results_page=0
		results_per_page=params.get('results_per_page')
		
		if results_per_page==None:
			results_per_page=default_results_per_page
		else:
			results_per_page=int(results_per_page)
		
		results_page=params.get('results_page')
		if results_page==None:
			results_page=default_results_page
		else:
			results_page=int(results_page)
		
		start_idx=results_page*results_per_page
		end_idx=(results_page+1)*results_per_page
		
		
		### NOW THE REAL VARIABLES
		#the base queryset contains all voyages
		#on stacking query vars: https://docs.djangoproject.com/en/3.2/topics/db/queries/#querysets-are-lazy
		queryset=Voyage.objects.all()

		####VOYAGE_ID (comma-delimited integers)
		if voyage_ids!=None:
			voyage_id=[i for i in voyage_ids.split(',')]
			queryset = queryset.filter(voyage_id__in=voyage_id)
		
		
		
		
		
		
		read_serializer=VoyageSerializer(queryset[start_idx:end_idx],many=True,fields=selected_query_fields)
		
		return JsonResponse(read_serializer.data,safe=False)
