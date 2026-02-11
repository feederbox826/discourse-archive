from db import create_tables, close
from download import test_latest, create_index

def main():
  create_tables()
  test_latest()
  create_index()
  close()

if __name__ == "__main__":
  main()