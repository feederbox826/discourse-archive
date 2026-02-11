import sqlite3
# local iports
from env import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# set wal
cur.execute('PRAGMA journal_mode=WAL;')
conn.commit()

# create
def create_tables():
  cur.execute('''
    CREATE TABLE IF NOT EXISTS topics (
      id INTEGER PRIMARY KEY,
      slug TEXT,
      title TEXT,
      created_at INTEGER,
      updated_at INTEGER,
      highest_post_number INTEGER
    );
  ''')
  conn.commit()
  cur.executescript('''
    CREATE INDEX IF NOT EXISTS idx_topics_updated_at ON topics (updated_at);
    CREATE INDEX IF NOT EXISTS idx_topics_highest_post_number ON topics (highest_post_number);
  ''')
  conn.commit()

def close():
  conn.execute('VACUUM;')
  conn.commit()
  conn.close()

# topics
def add_topic(topic):
  cur.execute('''
    INSERT OR REPLACE INTO topics (id, title, slug, created_at, updated_at, highest_post_number)
    VALUES (?, ?, ?, ?, ?, ?);
  ''', (topic['id'], topic['title'], topic['slug'], topic['created_at'], topic['last_posted_at'], topic['highest_post_number']))
  conn.commit()

def check_topic_updated(topic):
  cur.execute('''
    SELECT updated_at, highest_post_number
    FROM topics
    WHERE id = ?;
  ''', (topic['id'],))
  row = cur.fetchone()
  if row is None:
    return False
  db_updated_at, db_highest_post_number = row
  return topic['last_posted_at'] == db_updated_at and topic['highest_post_number'] == db_highest_post_number

def get_index():
  cur.execute('''
    SELECT id, slug, title, updated_at, highest_post_number
    FROM topics ORDER BY updated_at DESC;
  ''')
  return cur.fetchall()