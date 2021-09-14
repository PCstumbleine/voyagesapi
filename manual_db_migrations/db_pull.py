import mysql.connector
import json
import re
import os




d=open("dbcheckconf.json","r")
t=d.read()
d.close()
conf=json.loads(t)

cnx = mysql.connector.connect(**conf)
cursor = cnx.cursor()

old_db_name="voyages_staging"

cursor.execute("show tables from %s;" %old_db_name)
tables=cursor.fetchall()

new_db_name="voyages"

td={}

for table in tables:
	cursor.execute("show columns from %s;" %table)
	res=cursor.fetchall()
	column_names=[i[0] for i in res]
	td[table]=column_names

os.rename('db_shift.csv','db_shift.csv-backup')

d=open('db_shift.csv','a')
for t in td:
	d.write(old_db_name+'.'+t[0]+','+new_db_name+'.'+t[0]+'\n')
	for c in td[t]:
		d.write(c+','+c+'\n')
	d.write('\n')
