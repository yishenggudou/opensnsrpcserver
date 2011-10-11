# Copyright 2010 Google Inc.
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

import os
import sys
import traceback
import getopt

#
# Load Buzz library (if available...)
#

try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    import buzz
except ImportError:
    print 'Error importing Buzz library!!!'

print '-' * 80
print __doc__
print '-' * 80

token = verification_code = buzz_client = ''

#
# Function to obtain login data
#

def GetLoginData():
    'Obtains login information from either the command line or by querying the user'

    global token, verification_code, buzz_client
    key = secret = ''

    # Check first if anything is specified in the command line

    if len(sys.argv[1:]):
        try:
            (opts, args) = getopt.getopt(sys.argv[1:], 'k:s:v:', ['key','secret', 'vercode'])
            if (len(args)):        raise getopt.GetoptError('bad parameter')

        except getopt.GetoptError:
            print '''
Usage:    %s <-t access token> <-a verification_code>

-k (--key):        OPTIONAL, previously obtained access token key
-s (--secret):        OPTIONAL, previously obtained access token secret

Exiting...
            ''' % (sys.argv[0])
            sys.exit(0)

        for (opt, arg) in opts:
            if opt in ('-k', '--key'):
                key = arg
            elif opt in ('-s', '--secret'):
                secret = arg

    # Query the user for data otherwise - we need key and secret for our OAuth request token.

    if ((key == '') or (secret == '')):
        token = buzz_client.fetch_oauth_request_token ('oob')
        token = buzz_client.oauth_request_token

        print '''
Please access the following URL to confirm access to Google Buzz:

%s

Once you're done enter the verification code to continue: ''' % (buzz_client.build_oauth_authorization_url(token)),

        verification_code = raw_input().strip()
        buzz_client.fetch_oauth_access_token (verification_code, token)
    else:
        buzz_client.build_oauth_access_token(key, secret)

    # Do we have a valid OAUth access token?

    if (buzz_client.oauth_token_info().find('Invalid AuthSub signature') != (-1)):
        print 'Access token is invalid!!!'
        sys.exit(0)
    else:
        print """
Your access token key is \'%s\', secret is \'%s\'
Keep this data handy in case you want to reuse the session later!
""" % (buzz_client.oauth_access_token.key, buzz_client.oauth_access_token.secret)

def print_comment(comment):
    print """
Comment ID:     %s
Published:      %s
Updated:        %s
""" % (comment.id, comment.published, comment.updated)

def print_post(post):
    print """Post Link:        %s""" % (post.link.uri)

def print_person(person):
  print """Person ID:   %s""" % (person.id)
#
# Main program starts here
#

try:
    buzz_client = buzz.Client()
    buzz_client.oauth_scopes=[buzz.FULL_ACCESS_SCOPE]
    buzz_client.use_anonymous_oauth_consumer()

    # Search doesn't need any credentials. If this fails there's no point trying the rest.
    for count,data in enumerate(buzz_client.search('open.spotify.com')):
      print '(%s)' % (count+1),
      print_post(data)

    GetLoginData()

    print 'googlebuzz is following'
    for count, data in enumerate(buzz_client.following('googlebuzz')):
      print '(%s)' % (count+1),
      print_person(data)

    print 'sami.shalabi has these followers'
    for count, data in enumerate(buzz_client.followers('sami.shalabi')):
      print '(%s)' % (count+1),
      print_person(data)

    print 'adewale has commented on these posts'
    for count, data in enumerate(buzz_client.commented_posts('adewale')):
      print '(%s)' % (count+1),
      print_post(data)

    print 'This post had the following comments'
    for count, data in enumerate(buzz_client.comments('tag:google.com,2010:buzz:z13gyftqiobxxv1l122wepbj3oqndvhm5')):
      print '(%s)' % (count+1),
      print_comment(data)

    print 'adewale has liked these posts'
    for count, data in enumerate(buzz_client.liked_posts('adewale')):
      print '(%s)' % (count+1),
      print_post(data)

    print 'This post had the following likers'
    for count, data in enumerate(buzz_client.likers('tag:google.com,2010:buzz:z12gybujdnrxufdwu04cdjyb3mjeulcwv3c')):
      print '(%s)' % (count+1),
      print_person(data)

    print 'adewale has made the following posts'
    for count, data in enumerate(buzz_client.posts(user_id='adewale')):
      print '(%s)' % (count+1),
      print_post(data)

except:
    print '\nBzzzz! Something broke!!!'
    print '-' * 50
    traceback.print_exc()
    print '-' * 50
