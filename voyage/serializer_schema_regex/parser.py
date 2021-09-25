import re
import json
d=open('serializer_repr.txt','r')
t=d.readlines()


def get_field_data(l):
	
	name,field_type,field_metadata=re.findall('\s+([a-z|A-Z|0-9|_]+) = ([A-Z|a-z]+)(.*)',l)[0]
	field_metadata_minimized=re.sub('[ \(\']','',field_metadata)
	fm_split=field_metadata.split(', ')
	fm_split_clean=[re.sub('[\(\'\)]','',i) for i in fm_split]
	fm_split_clean=[i.strip() for i in fm_split_clean]
	try:
		kv_pairs={i.split('=')[0]:i.split('=')[1] for i in fm_split_clean}
	except:
		kv_pairs=None
	return name,field_type,kv_pairs
	
blocks={}
major=None
for l in t:
	#print(l)
	if re.match('    [a-z|A-Z]',l):
		major_name,field_type,field_metadata=get_field_data(l)
		blocks[major_name]={'metadata':field_metadata,'subfields':{}}
	else:
		if re.match('        [a-z|A-Z]',l):
			minor_name,field_type,field_metadata=get_field_data(l)
			blocks[major_name]['subfields'][minor_name]={'field_type':field_type,'field_metadata':field_metadata}

#print(blocks)	
d.close()
d=open('serializer_structure.json','w')
d.write(json.dumps(blocks))
d.close()


errors=[]
for major in blocks:
	for minor in blocks[major]['subfields']:
		if 'field_type' in blocks[major]['subfields'][minor]:
			try:
				print('\t'.join([major+'__'+minor,blocks[major]['subfields'][minor]['field_type'],blocks[major]['subfields'][minor]['field_metadata']['label']]))
			except:
				errors.append(major+'__'+minor)

print('ERRORS:')
for i in errors:
	print(i)