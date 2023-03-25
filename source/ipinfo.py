import urllib
import json

url = "http://ip-api.com/json/208.80.152.201"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data
