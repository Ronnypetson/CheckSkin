from __future__ import print_function
import os
import json

json_fn = 'imgs_list.txt'

jsonFile = open(json_fn,'r')
values = json.load(jsonFile)
jsonFile.close()

for v in values:
    _id = v['_id']
    detail_fn = 'details/'+_id+'.json'
    dfile = open(detail_fn,'r')
    dvalues = json.load(dfile)
    dfile.close()
    d_type = dvalues['meta']['clinical']['benign_malignant']
    os.rename("thumbs/"+_id+".jpeg","thumbs/"+d_type+"/"+_id+".jpeg")

