# Copyright (C) 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Wolff Dobson'

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

import apiclient.discovery
import httplib2
import pprint
import os.path
import settings
import time
import urllib

def authorize_self(client_id='None', client_secret='None'):
  if client_id is None or client_secret is None:
    raise Exception('Please register at the API Console at: https://code.google.com/apis/console.  See README.txt for details!')

  flow = OAuth2WebServerFlow(
      client_id=client_id,
      client_secret=client_secret,
      scope='https://www.googleapis.com/auth/plus.me',
      user_agent='google-api-client-python-plus-cmdline/1.0',
      xoauth_displayname='Google Plus Client Example App'
      )

  #Remove this file if you want to do the OAuth2 dance again!
  credentials_file = 'plus_auth.dat'

  storage = Storage(credentials_file)
  if os.path.exists(credentials_file):
    credentials = storage.get()
  else:
    credentials = run(flow, storage)

  return credentials

def build_service(credentials, http, api_key=None):
  if ( credentials != None ):
    http = credentials.authorize(http)
  service = apiclient.discovery.build('plus', 'v1', http=http, developerKey=api_key)

  return service


def main():
  http = httplib2.Http()
  credentials = authorize_self(settings.CLIENT_ID,settings.CLIENT_SECRET)
  service = build_service(credentials,http)

  person = service.people().get(userId='me').execute(http)

  print "Got your ID: " + person['displayName']

  # Now, we can continue on unauthorized
  # I could continue using my authenticated service, of course
  # but for example we'll use a second unauth'd one
  httpUnauth = httplib2.Http()
  serviceUnauth = build_service(None, httpUnauth, settings.API_KEY)

  activities_doc = serviceUnauth.activities().list(userId=person['id'],collection='public').execute(httpUnauth)

  activities = []
  npt = None

  if 'items' in activities_doc:
    activities = activities_doc[ 'items' ]
    print "Retrieved %d activities" % len(activities_doc['items'])

  npt = activities_doc['nextPageToken']

  while ( npt != None ):
    activities_doc = serviceUnauth.activities().list(userId=person['id'],collection='public').execute(httpUnauth)

    if 'items' in activities_doc:
      activities += activities_doc['items']
      print "Retrieved %d more activities" % len(activities_doc['items'])

    if not 'nextPageToken' in activities_doc or activities_doc['nextPageToken'] == npt:
      "---Done"
      break

    npt = activities_doc['nextPageToken']

  print "----------------\nPublic activities count:", len(activities)
  print

  if len(activities) > 0:
    for item in activities:
      print '  activity\t', item['object']['content'][:40], item['id']

    # Now, ask for the first item on the list
    top_activity = serviceUnauth.activities().get(activityId=activities[0]['id']).execute(httpUnauth)

    print '\n\ntop activity: ' + top_activity['id'] + ': ' + top_activity['object']['content']

  print '\n\nSUCCESS: Everything worked'

if __name__=='__main__':
  main()
