import mysql.connector
import time
import json
import re

#THIS IS A FIX TO THE STRING FORMATTING OF TWO VARIABLES: imp_arrival_at_port_of_dis and imp_departed_africa
#BOTH ARE IN FORMAT ",,YYYY"
#FOR EFFICIENT DJANGO QUERIES (IN A SERIALIZER) WE NEED THAT TO BE STORED IN SQL
#SIMPLY PUSHING THESE VALUES INTO DUPLICATE FIELDS: imp_arrival_at_port_of_dis_year and imp_departed_africa_year
#BUT WE SHOULD DO THIS FOR OTHER DATE FIELDS AS WELL TO SIMPLIFY OUR QUERY LOGIC

d=open("dbcheckconf.json","r")
t=d.read()
d.close()
conf=json.loads(t)

cnx = mysql.connector.connect(**conf)
cursor = cnx.cursor()

column_map=[
	['imp_arrival_at_port_of_dis','imp_arrival_at_port_of_dis_year'],
	['imp_departed_africa','imp_departed_africa_year']
]

table='voyage_voyagedates'

for columnset in column_map:
	a,b=columnset
	cursor.execute("select id,%s from %s;" %(a,table))
	r=cursor.fetchall()
	for i in r:
		id,strvalue=i
		year=strvalue.split(',')[2]
		if year !='':
			cursor.execute("update %s set %s=%s where id=%s" %(table,b,str(year),str(id)))
			cnx.commit()

cnx.close()