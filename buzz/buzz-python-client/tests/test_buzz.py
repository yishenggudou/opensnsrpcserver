#!/usr/bin/python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import buzz
import time
import re
from pprint import pprint
try:
  import yaml
except (ImportError):
  sys.stderr.write('Please install PyYAML.\n')
  exit(1)
try:
  import nose
  from nose.tools import make_decorator
  NOSE_ENABLED = True
except (ImportError):
  NOSE_ENABLED = False

TEST_CONFIG = buzz.CLIENT_CONFIG

OAUTH_CONSUMER_KEY = TEST_CONFIG['oauth_consumer_key']
OAUTH_CONSUMER_SECRET = TEST_CONFIG['oauth_consumer_secret']
OAUTH_TOKEN_KEY = TEST_CONFIG['oauth_token_key']
OAUTH_TOKEN_SECRET = TEST_CONFIG['oauth_token_secret']

BUZZ_TESTING_ID = str(TEST_CONFIG['testing_id'])
BUZZ_TESTING_ACCOUNT = str(TEST_CONFIG['testing_account'])
BUZZ_TARGET_ID = str(TEST_CONFIG['testing_target_id'])
BUZZ_TARGET_ACCOUNT = str(TEST_CONFIG['testing_target_account'])
BUZZ_POST_ID = str(TEST_CONFIG['testing_post_id'])

CLIENT = buzz.Client()
CLIENT.build_oauth_consumer(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)
CLIENT.build_oauth_access_token(OAUTH_TOKEN_KEY, OAUTH_TOKEN_SECRET)

GOOGLEPLEX_LATITUDE = '37.421976'
GOOGLEPLEX_LONGITUDE = '-122.08437'

def dumpjson(test_method):
  def dumpjson_runner(*args, **kwargs):
    try:
      test_method(*args, **kwargs)
    except Exception, e:
      if hasattr(e, '_json'):
        print 'JSON:'
        pprint(e._json)
      exc_info = sys.exc_info()
      raise exc_info[1], None, exc_info[2]
  if NOSE_ENABLED:
    return make_decorator(test_method)(dumpjson_runner)
  else:
    return dumpjson_runner

def clear_posts():
  # Make sure we don't have any posts
  posts = CLIENT.posts()
  for post in posts:
    assert ('CLIENTTEST: ' in post.content), 'Missing testing guard.  Abort.'
    CLIENT.delete_post(post)
  post = CLIENT.post(post_id=BUZZ_POST_ID).data
  post.unlike()
  post.unmute()

def create_post():
  post = buzz.Post(content="CLIENTTEST: This is a test post.")
  CLIENT.create_post(post)
  time.sleep(0.5)
  return CLIENT.posts().data[0]

def assert_list(obj):
  assert isinstance(obj, list), \
    "Should have been a list but was: %s of type: %s" % (obj, type(obj))

def assert_populated_list(obj, msg="Should have been a list with more than 0 items in it"):
  assert_list(obj)
  assert len(obj) > 0, msg

# For the most part, these tests do not rely on any specific piece of data
# being returned by the API.  Mostly they verify that an exception has not
# been thrown.  Not ideal, but better than needlessly brittle tests.

@dumpjson
def test_auth_required():
  client = buzz.Client()
  try:
    client.person().data
    assert False, "Authorization should have been required."
  except:
    assert True, "Great, it worked."

@dumpjson
def test_anonymous_consumer():
  client = buzz.Client()
  client.use_anonymous_oauth_consumer()
  client.oauth_scopes.append(buzz.FULL_ACCESS_SCOPE)
  request_token = \
    client.fetch_oauth_request_token('http://example.com/callback/')
  assert request_token.key, "Request token key missing."
  assert request_token.secret, "Request token secret missing."
  assert client.build_oauth_authorization_url(), \
    "Could not build authorization URL"

@dumpjson
def test_registered_consumer():
  client = buzz.Client()
  client.build_oauth_consumer(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)
  client.oauth_scopes.append(buzz.FULL_ACCESS_SCOPE)
  request_token = \
    client.fetch_oauth_request_token('http://example.com/callback/')
  assert request_token.key, "Request token key missing."
  assert request_token.secret, "Request token secret missing."
  assert client.build_oauth_authorization_url(), \
    "Could not build authorization URL"

@dumpjson
def test_person_me():
  result = CLIENT.person()
  person = result.data
  assert person, "Could not obtain reference to the token's account."
  assert person.name, \
    "Could not obtain reference to the account's display name."
  assert person.uri, \
    "Could not obtain reference to the account's profile link."

@dumpjson
def test_person_other():
  result = CLIENT.person(BUZZ_TESTING_ID)
  person = result.data
  assert person, "Could not obtain reference to the token's account."
  assert person.name, \
    "Could not obtain reference to the account's display name."
  assert person.uri, \
    "Could not obtain reference to the account's profile link."

@dumpjson
def test_person_me_without_auth():
  client = buzz.Client()
  try:
    client.person()
    assert False, "Authorization should have been required."
  except:
    assert True, "Great, it worked."

@dumpjson
def test_person_other_without_auth():
  client = buzz.Client()
  try:
    client.person(BUZZ_TESTING_ID)
    assert False, "Authorization should have been required."
  except:
    assert True, "Great, it worked."

@dumpjson
def test_followers_me():
  result = CLIENT.followers()
  followers = result.data
  assert_list(followers)

@dumpjson
def test_followers_paginates():
  client = buzz.Client()
  result = client.followers('googlebuzz')
  for count, person in enumerate(result):
    if count > buzz.DEFAULT_PAGE_SIZE:
      break
  else:
    # Poor man's fail() replacement
    assert False, \
    "Official Google Buzz account should have more than %s followers not %s" \
    % (buzz.DEFAULT_PAGE_SIZE, follower_count)

@dumpjson
def test_following_paginates():
  client = buzz.Client()
  result = client.following('googlebuzz')
  for count, person in enumerate(result):
    if count > buzz.DEFAULT_PAGE_SIZE:
      break
  else:
    # Poor man's fail() replacement
    assert False, \
    "Official Google Buzz account should be following more than %s people" \
    " not %s" % (buzz.DEFAULT_PAGE_SIZE, following_count)

@dumpjson
def test_followers_other():
  client = buzz.Client()
  result = client.followers(BUZZ_TESTING_ID)
  followers = result.data
  assert_list(followers)

@dumpjson
def test_following_me():
  result = CLIENT.following()
  following = result.data
  assert_list(following)

@dumpjson
def test_following_other():
  client = buzz.Client()
  result = client.following(BUZZ_TESTING_ID)
  following = result.data
  assert_list(following)

@dumpjson
def test_follow():
  person = CLIENT.person(BUZZ_TARGET_ID).data
  person.follow()
  # Give the API time to catch up
  time.sleep(1.5)
  followers = list(CLIENT.followers(BUZZ_TARGET_ID))
  assert BUZZ_TESTING_ID in [follower.id for follower in followers], \
    "Should have been able to find the account in followers list of %s items." % len(followers)
  following = CLIENT.following(BUZZ_TESTING_ID).data
  assert BUZZ_TARGET_ID in [followee.id for followee in following], \
    "Should have been able to find the target in following list."
  CLIENT.unfollow(BUZZ_TARGET_ID)

@dumpjson
def test_unfollow():
  person = CLIENT.person(BUZZ_TARGET_ID).data
  person.follow()
  person.unfollow()
  # Give the API time to catch up
  time.sleep(1.5)
  followers = CLIENT.followers(BUZZ_TARGET_ID).data
  assert not BUZZ_TESTING_ID in [follower.id for follower in followers], \
    "Should not have been able to find the account in followers list."
  following = CLIENT.following(BUZZ_TESTING_ID).data
  assert not BUZZ_TARGET_ID in [followee.id for followee in following], \
    "Should not have been able to find the target in following list."

@dumpjson
def test_follow_without_auth():
  client = buzz.Client()
  try:
    client.follow(BUZZ_TARGET_ID)
    assert False, "Authorization should have been required."
  except:
    assert True, "Great, it worked."

@dumpjson
def test_unfollow_without_auth():
  client = buzz.Client()
  try:
    client.unfollow(BUZZ_TARGET_ID)
    assert False, "Authorization should have been required."
  except:
    assert True, "Great, it worked."

@dumpjson
def test_people_search():
  client = buzz.Client()
  result = client.people_search("googlebuzzteam")
  people = result.data
  assert_populated_list(people, "Not enough people.")
  for person in people:
    assert isinstance(person, buzz.Person), \
      "Could not obtain reference to the person."      

@dumpjson
def test_people_search_by_topic_location():
  client = buzz.Client()
  result = client.people_search_by_topic(
    latitude=GOOGLEPLEX_LATITUDE,
    longitude=GOOGLEPLEX_LONGITUDE,
    radius=1000
  )
  people = result.data
  assert_populated_list(people, "Not enough people.")
  for person in people:
    assert isinstance(person, buzz.Person), \
      "Could not obtain reference to the person."

@dumpjson
def test_search_location():
  client = buzz.Client()
  result = client.search(
    latitude=GOOGLEPLEX_LATITUDE,
    longitude=GOOGLEPLEX_LONGITUDE,
    radius=1000
  )
  posts = result.data
  assert_populated_list(posts, "Not enough posts.")
  for post in posts:
    assert isinstance(post, buzz.Post), \
      "Could not obtain reference to the post."

@dumpjson
def test_search_query():
  client = buzz.Client()
  result = client.search(query="google")
  posts = result.data
  assert_populated_list(posts, "Not enough posts.")
  for i, post in enumerate(posts):
    assert isinstance(post, buzz.Post), \
      "Could not obtain reference to the post."
    if i >= 5:
      break

@dumpjson
def test_search_query_results_can_be_restricted():
  client = buzz.Client()
  max_results = 2
  result = client.search(query="google", max_results=max_results)
  posts = result.data
  assert_populated_list(posts, "Not enough posts.")
  assert max_results == len(posts)

@dumpjson
def test_posts_me():
  result = CLIENT.posts()
  posts = result.data
  assert isinstance(posts, list), \
    "Could not obtain reference to the account's posts."
  for post in posts:
    assert isinstance(post, buzz.Post), \
      "Could not obtain reference to the post."

@dumpjson
def test_posts_other():
  client = buzz.Client()
  result = client.posts(type_id='@public', user_id=BUZZ_TESTING_ID)
  posts = result.data
  assert isinstance(posts, list), \
    "Could not obtain reference to the account's posts."
  for post in posts:
    assert isinstance(post, buzz.Post), \
      "Could not obtain reference to the post."

@dumpjson
def test_consumption_me():
  result = CLIENT.posts(type_id='@consumption')
  posts = result.data
  assert isinstance(posts, list), \
    "Could not obtain reference to the account's posts."
  for post in posts:
    assert isinstance(post, buzz.Post), \
      "Could not obtain reference to the post."

@dumpjson
def test_consumption_other():
  client = buzz.Client()
  try:
    client.posts(type_id='@consumption', user_id=BUZZ_TESTING_ID).data
    assert False, "Consumption feeds should only be available for @me."
  except:
    assert True, "Great, it worked."

@dumpjson
def test_post():
  client = buzz.Client()
  result = client.post(post_id=BUZZ_POST_ID)
  post = result.data
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."

@dumpjson
def test_create_post():
  clear_posts()
  time.sleep(1.5)
  post = create_post()
  assert post.content == "CLIENTTEST: This is a test post."
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."

@dumpjson
def test_create_post_with_link():
  clear_posts()
  time.sleep(1.5)
  link_attachment = buzz.Attachment(
    type='article',
    title='Google',
    uri='http://www.google.com/'
  )
  post = buzz.Post(
    content='CLIENTTEST: This is a test post.',
    attachments=[
      link_attachment
    ]
  )
  CLIENT.create_post(post)
  time.sleep(0.5)
  post = CLIENT.posts().data[0]
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."
  assert post.content == 'CLIENTTEST: This is a test post.'
  assert_populated_list(
    post.attachments,
    'Could not obtain attachments.'
  )
  assert post.attachments[0].type == 'article'

@dumpjson
def test_create_post_with_photo():
  clear_posts()
  time.sleep(1.5)
  photo_link = buzz.Link(
    type='image/png',
    uri='http://upload.wikimedia.org/wikipedia/commons/3/30/Googlelogo.png'
  )
  photo_attachment = buzz.Attachment(
    type='photo',
    enclosure=photo_link
  )
  post = buzz.Post(
    content='CLIENTTEST: This is a test post.',
    attachments=[
      photo_attachment
    ]
  )
  CLIENT.create_post(post)
  time.sleep(0.5)
  post = CLIENT.posts().data[0]
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."
  assert post.content == 'CLIENTTEST: This is a test post.'
  assert_populated_list(
    post.attachments,
    'Could not obtain attachments.'
  )
  assert post.attachments[0].type == 'photo'

# TODO(ade)
# This test is commented out because of a bug in the Buzz API back-end
# It will be added back once the back-end bug is fixed.
#@dumpjson
#def test_create_post_with_video():
#  clear_posts()
#  time.sleep(1.5)
#  video_attachment = buzz.Attachment(
#    type='video',
#    uri='http://www.youtube.com/watch?v=nnsSUqgkDwU'
#  )
#  post = buzz.Post(
#    content='CLIENTTEST: This is a test post.',
#    attachments=[
#      video_attachment
#    ]
#  )
#  CLIENT.create_post(post)
#  time.sleep(0.5)
#  post = CLIENT.posts().data[0]
#  assert isinstance(post, buzz.Post), \
#    "Could not obtain reference to the post."
#  assert post.content == 'CLIENTTEST: This is a test post.'
#  assert_populated_list(
#    post.attachments,
#    'Could not obtain attachments.'
#  )
#  assert post.attachments[0].type == 'video'

@dumpjson
def test_create_post_with_geocode():
  clear_posts()
  time.sleep(1.5)
  post = buzz.Post(
    content='CLIENTTEST: This is a test post.',
    geocode=('37.422', '-122.0843')
  )
  CLIENT.create_post(post)
  time.sleep(0.5)
  post = CLIENT.posts().data[0]
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."
  assert post.content == 'CLIENTTEST: This is a test post.'
  assert str(post.geocode[0]) == '37.422'
  assert str(post.geocode[1]) == '-122.0843'

@dumpjson
def test_create_post_with_seven_bit_character_set():
  post = None
  try:
    clear_posts()
    time.sleep(1.5)
    seven_bit_character_set=''
    for c in xrange(128):
      seven_bit_character_set += chr(c)
    post = buzz.Post(content='CLIENTTEST: ' + seven_bit_character_set)
    CLIENT.create_post(post)
    time.sleep(0.5)
    post = CLIENT.posts().data[0]
    assert isinstance(post, buzz.Post), \
      "Could not obtain reference to the post."
  finally:
    try:
      clear_posts()
    except:
      # Could not clean up posts. No-op.
      None

@dumpjson
def test_created_post_has_published_field():
  clear_posts()
  time.sleep(1.5)
  post = create_post()
  assert post.published is not None
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."

@dumpjson
def test_update_post():
  clear_posts()
  post = create_post()
  assert ('CLIENTTEST: ' in post.content), 'Missing testing guard.  Abort.'
  post.content = "CLIENTTEST: This is updated content."
  time.sleep(1.5)
  CLIENT.update_post(post)
  time.sleep(1.5)
  post = CLIENT.posts().data[0]
  assert post.content == "CLIENTTEST: This is updated content."
  assert isinstance(post, buzz.Post), \
    "Could not obtain reference to the post."

@dumpjson
def test_delete_post():
  create_post()
  time.sleep(1.5)
  clear_posts()
  time.sleep(3.0)
  assert CLIENT.posts().data == []

@dumpjson
def test_comments():
  client = buzz.Client()
  result = client.comments(post_id=BUZZ_POST_ID)
  comments = result.data
  assert isinstance(comments, list), \
    "Could not obtain reference to the account's posts."
  for comment in comments:
    assert isinstance(comment, buzz.Comment), \
      "Could not obtain reference to the comment."

@dumpjson
def test_create_comment():
  clear_posts()
  post = create_post()
  time.sleep(3.0)
  comment = buzz.Comment(
    content="CLIENTTEST: This is a test comment.", post_id=post.id
  )
  CLIENT.create_comment(comment)
  time.sleep(2.5)
  comments = post.comments().data
  assert isinstance(comments, list), \
    "Could not obtain reference to the account's posts."
  comment = comments[0]
  assert isinstance(comment, buzz.Comment), \
    "Could not obtain reference to the comment."
  assert comment.content == "CLIENTTEST: This is a test comment."

@dumpjson
def test_update_comment():
  clear_posts()
  post = create_post()
  comment = buzz.Comment(
    content="CLIENTTEST: This is a test comment.", post_id=post.id
  )
  CLIENT.create_comment(comment)
  time.sleep(3.0)
  comment = post.comments().data[0]
  comment.content = "CLIENTTEST: This is updated content."
  CLIENT.update_comment(comment)
  time.sleep(2.5)
  comment = post.comments().data[0]
  assert comment.content == "CLIENTTEST: This is updated content."

@dumpjson
def test_delete_comment():
  clear_posts()
  post = create_post()
  time.sleep(3.0)
  comment = buzz.Comment(
    content="CLIENTTEST: This is a test comment.", post_id=post.id
  )
  CLIENT.create_comment(comment)
  time.sleep(2.5)
  comments = post.comments().data
  comment = comments[0]
  assert comments != []
  CLIENT.delete_comment(comment)
  time.sleep(2.5)
  comments = post.comments().data
  assert comments == []

@dumpjson
def test_related_links():
  clear_posts()
  client = buzz.Client()
  post = client.post(post_id=BUZZ_POST_ID).data
  links = post.related_links().data
  assert isinstance(links, list), \
    "Could not obtain reference to the post's related links."
  assert len(links) > 0, \
    "Not enough related links for the post."

@dumpjson
def test_commented_posts():
  clear_posts()
  post = create_post()
  time.sleep(1.5)
  comment = buzz.Comment(
    content="CLIENTTEST: This is a test comment.", post_id=post.id
  )
  CLIENT.create_comment(comment)
  assert len(CLIENT.commented_posts().data) > 0

@dumpjson
def test_like_post():
  clear_posts()
  post = CLIENT.post(post_id=BUZZ_POST_ID).data
  post.like()
  time.sleep(3.0)
  posts = CLIENT.liked_posts().data
  assert len(posts) == 1
  clear_posts()

@dumpjson
def test_unlike_post():
  clear_posts()
  post = CLIENT.post(post_id=BUZZ_POST_ID).data
  post.like()
  time.sleep(2.5)
  posts = CLIENT.liked_posts().data
  assert len(posts) == 1
  post.unlike()
  time.sleep(3.0)
  posts = CLIENT.liked_posts().data
  assert len(posts) == 0
  clear_posts()

@dumpjson
def test_post_likers():
  post = CLIENT.post(post_id=BUZZ_POST_ID).data
  likers = post.likers().data
  assert_populated_list(likers, "Should have more than 0 likers")

@dumpjson
def test_mute_post():
  clear_posts()
  post = CLIENT.post(post_id=BUZZ_POST_ID).data
  # Make sure it doesn't error out
  post.mute()

@dumpjson
def test_unmute_post():
  clear_posts()
  post = CLIENT.post(post_id=BUZZ_POST_ID).data
  post.mute()
  # Make sure it doesn't error out
  post.unmute()

@dumpjson
def test_share_count():
  count = CLIENT.share_count('http://www.google.com/')
  assert count > 0

if __name__ == '__main__':
  if NOSE_ENABLED:
    config = nose.config.Config(includeExe=True, verbosity=3)
    nose.main(config=config)
  else:
    sys.stderr.write('Please install nose.\n')
    exit(1)
