from django.shortcuts import render
from django.db.models import Q,Prefetch
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import json
from .models import Voyage
from .serializers import VoyageSerializer
from .fields import *


#lookups: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups

class VoyageList(APIView):
	
	def get(self,request):
		params=self.request.query_params
		
		#FIELD SELECTION
		## selected_fields
		### this is important because responses can quickly become large enough (not on the SQL side but on spitting them back out) to dramatically slow the response time
		selected_fields=params.get('selected_fields')
		if selected_fields!=None:
			selected_query_fields=(i for i in selected_fields.split(','))
		else:
			selected_query_fields=None
		
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

		####VOYAGE_ID COMMA-SEPARATED INTEGERS
		#now we just have to enumerate our varibles and build filters for them.
		voyage_ids=params.get('voyage_ids')
		if voyage_ids!=None:
			voyage_id=[int(i) for i in voyage_ids.split(',')]
			queryset = queryset.filter(voyage_id__in=voyage_id)
		
		
		#the below variables (numeric_fields, text_fields) are defined in fields.py
		active_numeric_search_fields=[i for i in set(params).intersection(set(numeric_fields))]
		
		if len(active_numeric_search_fields)>0:
		
			for field in active_numeric_search_fields:
				min,max=[float(i) for i in params.get(field).split(',')]
				kwargs = {
				'{0}__{1}'.format(field, 'lte'): max,
				'{0}__{1}'.format(field, 'gte'): min
				}
			queryset=queryset.filter(**kwargs)
		
		active_text_search_fields=[i for i in set(params).intersection(set(text_fields))]
		if len(active_text_search_fields)>0:
			for field in active_text_search_fields:
				searchstring=params.get(field)
				kwargs = {
				'{0}__{1}'.format(field, 'icontains'): searchstring
				}
			print(kwargs)
			queryset=queryset.filter(**kwargs)
		
		
		read_serializer=VoyageSerializer(queryset[start_idx:end_idx],many=True,selected_fields=selected_query_fields)
		
		def get_serializer_context(self):
			return {'request': self.request}
		
		return JsonResponse(read_serializer.data,safe=False)
