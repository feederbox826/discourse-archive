from dotenv import load_dotenv
load_dotenv()

from os import getenv
URL_BASE = getenv("DISCOURSE_URL_BASE", "https://discourse.stashapp.cc")
# default to 5s, less than 0.3 will result in ratelimits
# https://meta.discourse.org/t/78612
RATELIMIT = max(float(getenv("DISCOURSE_RATELIMIT", "5")), 0.3)
DOWNLOAD_DIR = getenv("DOWNLOAD_DIR", "data/topics")
DB_PATH = getenv("DOWNLOAD_DB", "data/topics.db")

# can be string or bool, try converting to bool first, then fallback to path
DISCOURSE_SSL = getenv("DISCOURSE_VALIDATE_SSL")
VALIDATE_SSL = True
if DISCOURSE_SSL is not None:
  if DISCOURSE_SSL.lower() in ("true", "1", "t"):
    VALIDATE_SSL = True
  elif DISCOURSE_SSL.lower() in ("false", "0", "f"):
    VALIDATE_SSL = False
  else:
    VALIDATE_SSL = DISCOURSE_SSL