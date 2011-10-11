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
import logging
import os
import sys
import traceback

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

def print_post(post):
    print """
Post ID:        %s
Title:          %s
Actor:          %s
Content         %s
Published:      %s
Updated:        %s
URI:            %s
""" % (post.id, post.title, post.actor.name, post.content, post.published, post.updated, post.link)

#
# Main program starts here
#

try:
    buzz_client = buzz.Client()

    print '\nNow let\'s get the search term. Please enter search term\' (ENTER for \"open.spotify.com\"): ',
    search_term = raw_input().strip()
    if (search_term == ''): search_term = 'open.spotify.com'

    print 'Searching for [%s]' % search_term
    results = buzz_client.search(search_term)
    print 'Search results: '
    for index,data in enumerate(results):
        print index
        print_post(data)
except:
    print '\nBzzzz! Something broke!!!'
    print '-' * 50
    traceback.print_exc()
    print '-' * 50
