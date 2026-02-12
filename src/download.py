
import json
import time
import itertools
# local imports
from client import discourse
from db import check_topic_updated, add_topic, get_index, commit
from env import URL_BASE, RATELIMIT, DOWNLOAD_DIR

SEPERATORS = (',', ':') # for json dumps, no spaces to save space

def get_latest(page):
  latest = discourse.get(f"{URL_BASE}/latest.json?page={page}&per_page=50").json()
  return latest['topic_list']['topics']

def download_stream(topic):
  print("Downloading partial posts for topic")
  # first, get id of all posts already downloaded
  topic_ids = set()
  for post in topic['post_stream']['posts']:
    topic_ids.add(post['id'])
  stream_ids = set(topic['post_stream']['stream'])
  # missing posts
  # sort by id to match order in stream
  missing_ids = sorted(stream_ids.difference(topic_ids))
  appended_posts = []
  # batch into 20s
  for batch in list(itertools.batched(missing_ids, 20)):
    query_url = "&post_ids[]=".join(str(post_id) for post_id in batch)
    post_data = discourse.get(f"{URL_BASE}/t/{topic['id']}/posts.json?post_ids[]={query_url}").json()
    print(f"Downloaded posts {batch[0]}-{batch[-1]} for topic {topic['id']}")
    appended_posts.extend(post_data['post_stream']['posts'])
    time.sleep(RATELIMIT) # sleep to avoid rate limit
  # add all missing posts to topic
  topic['post_stream']['posts'].extend(appended_posts)
  # delete stream
  del topic['post_stream']['stream']
  return topic

def download_topic(topic_id, stream=False):
  download_url = f"{URL_BASE}/t/{topic_id}.json?include_suggested=false"
  topic = discourse.get(download_url).json()
  # if 404, skip
  if 'errors' in topic:
    print(f"Topic {topic_id} {topic['errors']} - skipping")
    return
  filename = f"{DOWNLOAD_DIR}/{topic_id}.json"
  if (stream): # if stream, read stream
    topic = download_stream(topic)
  # write topic to file
  with open(filename, "w", encoding="utf-8") as f:
    f.write(json.dumps(topic, separators=SEPERATORS))
  # yes, update would be better, but i'm lazy
  add_topic(topic)

def test_latest(page=0):
  topics = get_latest(page)
  # if all topics not latest, get next page
  outdated_count = 0
  for topic in topics:
    # check against database
    if not check_topic_updated(topic):
      outdated_count += 1
      print(f"Updating topic {topic['id']} - {topic['slug']}")
      # if post_count > 20, stream = true
      # discourse by default only returns 20
      download_topic(topic['id'], stream=topic['highest_post_number'] > 20)
      time.sleep(RATELIMIT)
  # check outdated_count
  # if last page
  topic_length = len(topics)
  if topic_length == 0:
    print("No more topics to check.")
  elif outdated_count == topic_length:
    print("All topics are outdated, checking next page...")
    test_latest(page + 1)
  commit() # commit at the very end
  print("Finished checking latest topics.")

def create_index():
  index = get_index()
  with open(f"{DOWNLOAD_DIR}/index.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(index, separators=SEPERATORS))