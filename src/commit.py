from pathlib import Path

from git import Repo
from datetime import datetime

from env import DOWNLOAD_DIR

def commit_and_push():
  print("Committing and pushing changes to git")
  repo = Repo(DOWNLOAD_DIR)
  download_path = Path(DOWNLOAD_DIR)
  json_files = [f.name for f in download_path.glob("*.json")]
  if json_files:
    repo.index.add(json_files)
  if repo.index.diff("HEAD"):
    repo.index.commit(f"Archive update: {datetime.now().isoformat()}")
    origin = repo.remote(name="origin")
    origin.push()