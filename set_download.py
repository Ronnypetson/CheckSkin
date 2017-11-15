from __future__ import print_function
import json

json_fn = 'imgs_list.txt'

jsonFile = open(json_fn,'r')
values = json.load(jsonFile)
jsonFile.close()

f = open('download.sh','w')
curl_1 = "curl -X GET --header 'Accept: image/jpeg' 'https://isic-archive.com/api/v1/image/"
curl_2 = "/thumbnail?width=50&height=50' -o thumbs/"
curl_3 = ".jpeg"
curl_d1 = "curl -X GET --header 'Accept: application/json' 'https://isic-archive.com/api/v1/image/"
curl_d2 = "' -o details/"
curl_d3 = ".json"
for v in values:
    #print(curl_1+v['_id']+curl_2+v['_id']+curl_3,file=f)
    print(curl_d1+v['_id']+curl_d2+v['_id']+curl_d3,file=f)

