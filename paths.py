import requests
import circuits
import json

URL = 'http://livetiming.formula1.com/static/'

# returns the year response
def get_year(year):
    resp = json.loads(requests.get(URL + year + '/Index.json').content)
    return resp

def get_meetings(circuit):
    return