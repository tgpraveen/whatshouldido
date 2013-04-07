import gflags
import httplib2
import json
import urllib
import datetime

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

#Specific to Python 2.x
#In Python 3.x the below line needs to be changed.
#from urlparse import urlencode

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='488136451036-lro31l0o6a1ik8311ephauicc6mbsujg.apps.googleusercontent.com',
    client_secret='lxv2BxU4Dftal8H7PCIfjQZC',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='whatshouldido')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='AIzaSyDfaaRfNmGVgoS7j65djnsqPpA1PK2LYeU')
#print 'Hello'
#event = {
#  'summary': 'Appointment',
#  'location': 'Somewhere',
#  'start': {
#    'dateTime': '2013-06-03T10:00:00.000-07:00'
#  },
#  'end': {
#    'dateTime': '2013-06-03T10:25:00.000-07:00'
#  }
#}

#created_event = service.events().insert(calendarId='primary', body=event).execute()
#created_event = service.events().insert(calendarId='primary', body=event).execute()
#service.events().
#calendar = service.calendars().get(calendarId='primary').execute()
#print calendar['summary']
#print created_event['id']

#resp, content = http.request("https://www.googleapis.com/calendar/v3/calendars/primary", "GET")
resp, content = http.request("https://www.googleapis.com/calendar/v3/users/me/calendarList/?key=AIzaSyDfaaRfNmGVgoS7j65djnsqPpA1PK2LYeU", "GET")
#print content
#print type(content)
jsoncontent = json.loads(content)
#print jsoncontent["items"]
for ite in jsoncontent['items']:
	if 'primary' in ite:
		if ite['primary']:
			#print ite
			primaryid=ite['id']
			break

#print primaryid


#print 'timeMin'
#print datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")+'.000-07:00'
#print 'timeMax'
#print (datetime.datetime.now() + datetime.timedelta(1*365/12)).strftime("%Y-%m-%dT%H:%M:%S")+'.000-07:00'
#print 'tzinfo'
#print datetime.tzinfo.utcoffset(datetime.datetime.now())


body = {
	'items': [
	  {
		  'id': primaryid
		       }
			    ],
			    # 'timeMin': '2013-06-03T10:00:00.000-07:00',
			    # 'timeMax': '2013-07-03T10:00:00.000-07:00',
#			     from datetime import date
#			     from dateutil.relativedelta import relativedelta

			     #six_months = date.today() + relativedelta( months = +6 )
			     'timeMin': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")+'.000-07:00',
			     'timeMax': (datetime.datetime.now() + datetime.timedelta(1*365/12)).strftime("%Y-%m-%dT%H:%M:%S")+'.000-07:00'
       }

#body = {'timeMin': '2013-06-03T10:00:00.000-07:00'}
#body = {'timeMin': '2013-06-03T10:00:00.000-07:00'}


'''

{
      "items": [
      {"id": primaryid}
      ],
      "timeMin": "2013-05-03T10:00:00.000-07:00",
      "timeMax": "2013-07-03T10:00:00.000-07:00"
      }
      '''
#print body
#print urllib.urlencode(body)
#print json.dumps(body)
resp2, freebusycontent = http.request("https://www.googleapis.com/calendar/v3/freeBusy?key=AIzaSyDfaaRfNmGVgoS7j65djnsqPpA1PK2LYeU", "POST", json.dumps(body),headers={'content-type':'application/json'})

#urllib.urlencode
#print http.request("https://www.googleapis.com/calendar/v3/freeBusy", "POST", body = json.dumps(body))
#resp2, freebusycontent = http.request("https://www.googleapis.com/calendar/v3/freeBusy", "POST", body = json.dumps(body))
#resp2, freebusycontent = http.request("https://www.googleapis.com/calendar/v3/freeBusy", "POST", body)
#print "333"
#print freebusycontent
#print 'header'
#print resp
#print 'content'
#print content
freebusycontentjson=json.loads(freebusycontent)
location = {}
locationcounter = 0
prevendtime = ''
freeperiod = {}
freeperiodcounter = 0
#print "222"
#print freebusycontentjson['calendars'][primaryid]['busy']
for busyevent in freebusycontentjson['calendars'][primaryid]['busy']:
	#print locationcounter
	#print 'busyevent '
	#print busyevent
	#busyevent=json.loads(busyevent)
	#print busyevent
	thisstarttime = busyevent["start"]
	thisstarttime = thisstarttime.replace(':','%3A')
	freeperiod[freeperiodcounter] = -1
	from datetime import datetime
	from time import strptime
	if prevendtime != '':
		#print "111"
		#print(thisstarttime.replace('%3A',':'))
		thisstarttimedatetime =	datetime(*strptime(thisstarttime.replace('%3A',':')[:-1], "%Y-%m-%dT%H:%M:%S")[0:6])
		prevendtimedatetime = datetime(*strptime(prevendtime.replace('%3A',':')[:-1], "%Y-%m-%dT%H:%M:%S")[0:6])
		freeperiod[freeperiodcounter] = (thisstarttimedatetime-prevendtimedatetime).total_seconds()
	freeperiodcounter = freeperiodcounter + 1
	#print thisstarttime
	#thisstarttime = urllib.quote(thisstarttime, safe=":/")
	thisendtime = busyevent["end"]
	thisendtime = thisendtime.replace(':','%3A')
	#thisendtime = urllib.quote(thisendtime, safe=":/")
	#print 'thisstarttime '+urllib.urlencode(thisstarttime)
	resp3, content3 = http.request("https://www.googleapis.com/calendar/v3/calendars/"+primaryid+"/events?timeMax="+thisendtime+"&timeMin="+thisstarttime+"&key=AIzaSyDfaaRfNmGVgoS7j65djnsqPpA1PK2LYeU", "GET")
	#print "https://www.googleapis.com/calendar/v3/calendars/"+primaryid+"/events?timeMax="+thisendtime+"&timeMin="+thisstarttime+"&key=AIzaSyDfaaRfNmGVgoS7j65djnsqPpA1PK2LYeU"
	#print content3
	content3json = json.loads(content3)
	#print 'location'
	location[locationcounter] = ""
	prevendtime = thisendtime
	if 'location' in content3json['items'][0]:
		#print content3json['items'][0]['location']
		currentlocation = content3json['items'][0]['location']
		location[locationcounter] = currentlocation
	locationcounter = locationcounter + 1
print freeperiod
print location

		

