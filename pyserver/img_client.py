import requests

files = {'file': open('test.jpg', 'rb')}
r = requests.post('http://10.0.0.108:8000', files=files)
print r.request.headers

