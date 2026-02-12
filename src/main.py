from db import create_tables, close
from download import test_latest, create_index
from commit import commit_and_push

def main():
  create_tables()
  test_latest()
  create_index()
  commit_and_push()
  close()

if __name__ == "__main__":
  main()