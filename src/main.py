import argparse
import sched
import sys
import time

from db import create_tables, close
from download import test_latest, create_index
from commit import commit_and_push

def run():
  create_tables()
  test_latest()
  create_index()
  commit_and_push()
  close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--run-once", action="store_true", help="Run once and exit")
  args = parser.parse_args()

  if args.run_once:
    run()
    sys.exit(0)

  scheduler = sched.scheduler(time.time, time.sleep)

  def run_and_reschedule():
    try:
      run()
    except Exception as e:
      print(f"Error: {e}", file=sys.stderr)
    scheduler.enter(3600, 1, run_and_reschedule)
  scheduler.enter(0, 1, run_and_reschedule)
  scheduler.run()