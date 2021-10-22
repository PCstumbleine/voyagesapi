import mysql.connector
import time
import json
import re

#SO THE LOGIC HERE IS PRETTY STRAIGHTFORWARD
##I MAP THE OLD TABLES TO THE NEW TABLES
##WHERE POSSIBLE, I'VE DONE THIS IN A SINGLE COMMAND
##I HAVE RUN THIS LINE BY LINE WITH BASIC ERROR HANDLING & LOGGING
##I HAVE DROPPED DOUBLE-BIND FOREIGN KEYS, ALWAYS FAVORING THE TABLE THAT'S MORE CENTRAL (USUALLY, THIS SIMPLY MEANS THAT 'VOYAGES' KEEPS THE FK)
###SO NOW, FOR INSTANCE, YOU CAN ADD A SLAVESNUMNBERS ROW WITHOUT ATTACHING IT TO A VOYAGE
###BUT IT MAKES IMPORTATION POSSIBLE WITHOUT THE RIDICULOUS DANCE OF PURGING AND RE-APPLYING ALL FOREIGN KEYS, WHICH, OF COURSE, CAN OBSCURE ERRORS SUCH AS THE ABOVE
##I ALSO DECIDED TO DROP EXPLICIT ROWID PRIMARY KEYS FROM THE CONNECTION TABLES AND MAKE THEM EXPLICIT IN THE TABLES THEY CONNECT --E.G., ID MATCHES VOYAGE_ID IN THE VOYAGES TABLE IN ALL BUT ONE CASE. SO I COLLAPSED THESE.
###THIS WILL MAKE UPDATING THE DATABASE FROM WITHIN DJANGO MORE SEAMLESS
###BUT IT WILL ALSO REQUIRE THAT WHEN WE EXPORT AND REIMPORT, WE DO SO IN SUCH A WAY THAT THE PK'S ARE NOT AUTO-GENERATED AGAIN -- AS THAT WOULD CAUSE OUR VOYAGE_IDS TO DRIFT


def main(oldtable,newtable,columns):
	successes=0
	failures=0
	oldcolumns=[]
	newcolumns=[]
	#print(columns)
	for c in columns:
		o,n=c.split(",")
		oldcolumns.append(o)
		newcolumns.append(n)
	print("mapping %s to %s" %(oldtable,newtable))
	cursor.execute("select %s from %s;" %(','.join(oldcolumns),oldtable))
	res=cursor.fetchall()
	qmarkstr=','.join(["%s" for i in range(len(newcolumns))])
	newcolstr=','.join([n for n in newcolumns])
	newcolstr=re.sub('\'','',newcolstr)
	newcolstr=re.sub('\"','',newcolstr)
	execstr="insert into %s (%s) values (%s);" %(newtable,newcolstr,qmarkstr)
	for r in res:
		#print(execstr)
		#print(r)
		try:
			cursor.execute(execstr, r)
			cnx.commit()
			successes+=1
		except:
			failures+=1
			print("failed on: ", r)
	print('migrated %s to %s with %s successes and %s failures' %(oldtable,newtable,str(successes),str(failures)))
				

d=open("dbcheckconf.json","r")
t=d.read()
d.close()
conf=json.loads(t)

cnx = mysql.connector.connect(**conf)
cursor = cnx.cursor()

d=open("db_shift.csv",'r')
t=d.read()
d.close()

#clear out the non-linebreak whitespaces
#because the rest of this is going to be super fragile

#REQUIRES THERE TO BE A DOUBLE LINE BREAK, NO MORE NO LESS, BTW TABLES



t=re.sub("[ \t\r\f\v]","",t)
tables=t.split("\n\n")
tables=[t for t in tables if t!='']
foreign_key_constraints=[]



#drop foreign key constraints
FK_CONSTRAINTS=[]
for table in tables:
	oldtable,newtable=table.split('\n')[0].split(',')
	old_db=re.search("[^.]+",oldtable).group(0)
	new_db=re.search("[^.]+",newtable).group(0)
	q="show create table %s" %newtable
	cursor.execute(q)
	res=cursor.fetchall()
	pattern=re.compile("CONSTRAINT `([a-z|A-Z|0-9|_]+)` FOREIGN KEY \(`([a-z|A-Z|0-9|_]+)`\) REFERENCES `([a-z|A-Z|0-9|_]+)` \(`([a-z|A-Z|0-9|_]+)`\)")
	
	for r in res:
		source_table,create_table=r
		#print(create_table)
		table_fk_constraints=pattern.findall(create_table)
		for table_fk_constraint in table_fk_constraints:
			entry=[source_table]+list(table_fk_constraint)
			#print(entry)
			FK_CONSTRAINTS.append(entry)
#print(new_db)
#print(FK_CONSTRAINTS)

for fkc in FK_CONSTRAINTS:
	source_table,constraint_id,source_column,target_table,target_column=fkc
	q='alter table %s.%s drop foreign key `%s`;' %(new_db,source_table,constraint_id)
	print(q)
	cursor.execute(q)
	cnx.commit()




#now shift table entries
for table in tables:
	
	oldtable,newtable=table.split('\n')[0].split(',')
	columns=table.split('\n')[1:]
	main(oldtable,newtable,columns)


#now reinforce constraints'''
for fkc in FK_CONSTRAINTS:
	source_table,constraint_id,source_column,target_table,target_column=fkc
	q='alter table %s.%s add constraint %s foreign key (%s) references %s (%s);' %(new_db,source_table,constraint_id,source_column,target_table,target_column)
	print(q)
	cursor.execute(q)
	cnx.commit()

cnx.close()

