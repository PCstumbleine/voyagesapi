from django.shortcuts import render
from django.db.models import Q,Prefetch
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.metadata import SimpleMetadata
from rest_framework.response import Response
import json
from .models import Voyage
from .serializers import *

##This is already broken -- I need a way to get the fields & metadata off the serializer instance.
from .fields import *


#lookups: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups


def walker(schema,base_address,serializer):	
	#this one will dig into a schema and get what it can.
	#not fragile, but not smart.
	try:
		fields=serializer.fields.__dict__['fields']
		for field in fields:
			datatypestr=str(type(fields[field]))
		
			if base_address!='':
				address='__'.join([base_address,field])
			else:
				address=field
		
			if 'serializer' in datatypestr:
				schema=walker(schema,address,fields[field])
			else:
				label=fields[field].label
				schema[address]={'type':datatypestr,'label':label}
	except:
		print(base_address)
		
		#it does not capture the "through" fields
		#help(serializer)
	return schema


class VoyageList(generics.GenericAPIView):
	
	metadata_class=SimpleMetadata
	serializer_class=VoyageSerializer
	
	def options(self, request, *args, **kwargs):
		"""
		Handler method for HTTP 'OPTIONS' request.
		"""		
		#the below renders a flat schema, with double-underscores marking nested relations.
		#easy enough to unpack if that's what we want
		schema=walker({},base_address='',serializer=self.get_serializer())
		
		return JsonResponse(schema,safe=False)
        
	def get(self,request):
		queryset=Voyage.objects.all()
		
		params=self.request.query_params
		
		#FIELD SELECTION
		## selected_fields
		### currently can only select tables one level down -- all the subsidiary fields come with it
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
		
		return JsonResponse(read_serializer.data,safe=False)
