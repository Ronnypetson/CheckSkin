from __future__ import print_function
import os
import json
from random import randint
from shutil import copyfile

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
    if randint(1,5) == 5:
        d_type = "test/"+d_type
    #os.rename("thumbs/"+_id+".jpeg","thumbs/"+d_type+"/"+_id+".jpeg")
    if not os.path.isfile('thumbs/benign/'+_id+'.jpeg')\
     and not os.path.isfile('thumbs/malignant/'+_id+'.jpeg')\
     and not os.path.isfile('thumbs/test/benign/'+_id+'.jpeg')\
     and not os.path.isfile('thumbs/test/malignant/'+_id+'.jpeg'):
        copyfile("thumbs/"+_id+".jpeg","thumbs/"+d_type+"/"+_id+".jpeg")

