import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

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
#  print 'Hello'
#else:
#  print "Go fuck yourself"

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
event = {
  'summary': 'Appointment',
  'location': 'Somewhere',
  'start': {
    'dateTime': '2013-06-03T10:00:00.000-07:00'
  },
  'end': {
    'dateTime': '2013-06-03T10:25:00.000-07:00'
  }
}

#created_event = service.events().insert(calendarId='primary', body=event).execute()
created_event = service.events().insert(calendarId='primary', body=event).execute()

print created_event['id']
