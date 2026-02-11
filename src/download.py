
import time
from compression import zstd
# local imports
from client import discourse
from db import check_topic_updated, add_topic
from env import URL_BASE, RATELIMIT, DOWNLOAD_DIR

def get_latest(page):
  latest = discourse.get(f"{URL_BASE}/latest.json?page={page}&per_page=50").json()
  return latest['topic_list']['topics']

def download_topic(topic_id):
  # HEAD test
  head = discourse.head(f"{URL_BASE}/t/{topic_id}.json")
  if head.status_code == 404:
    print(f"Topic {topic_id} not found - skipping")
    return
  # grab topic
  topic = discourse.get(f"{URL_BASE}/t/{topic_id}.json").json()
  # if 404, skip
  if 'errors' in topic:
    print(f"Topic {topic_id} {topic['error_type']} - skipping")
    return
  slug = topic['slug']
  filename = f"{DOWNLOAD_DIR}/{topic_id}_{slug}.json.zstd"
  # write topic to file
  with open(filename, "wb") as f:
    compressed = zstd.compress(str(topic).encode('utf-8'), level=22)
    f.write(compressed)
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
      download_topic(topic['id'])
      # downloaded, sleep
      time.sleep(RATELIMIT)
  # check outdated_count
  # if last page
  if len(topics) == 0:
    print("No more topics to check.")
  elif outdated_count == len(topics):
    print("All topics are outdated, checking next page...")
    # get next page
    test_latest(page + 1)