import requests
# local import
from env import VALIDATE_SSL

discourse = requests.Session()
discourse.verify = VALIDATE_SSL
discourse.headers.update({"User-Agent": "discourse-archive/0.1 (feederbox.cc/gh/discourse-archive)"})