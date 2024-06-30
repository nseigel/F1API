import requests
import codecs
import json
import info as l

def find_meeting(circuit, year):
      url = 'http://livetiming.formula1.com/static/' + str(year) + '/Index.json'
      resp = requests.get(url)
      resp = json.loads(codecs.decode(resp.content, encoding='utf-8-sig'))
      key = l.circuits[circuit]
      meeting = {}
      for meet in resp['Meetings']:
            if meet["Code"] == key:
                  meeting = meet
      return meeting

def find_session(session, circuit, year):
      meeting = find_meeting(circuit, year)
      path = 'https://livetiming.formula1.com/static/'
      for sess in meeting["Sessions"]:
            try:
                  if sess["Name"] == session:
                        path += sess["Path"]
            except KeyError:
                  print('KeyError')
      return path