from db import create_tables
from download import test_latest

def main():
  create_tables()
  test_latest()

if __name__ == "__main__":
  main()