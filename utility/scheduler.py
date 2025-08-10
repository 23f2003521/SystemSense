import time
import logging
import signal
import sys
from config import CHECK_INTERVAL_MINUTES
from main import run_health_check_once

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def signal_handler(sig, frame):
    logging.info("Scheduler stopping gracefully.")
    sys.exit(0)

def start_scheduler():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logging.info(f"Starting scheduler with interval {CHECK_INTERVAL_MINUTES} minutes.")
    while True:
        try:
            run_health_check_once()
            logging.info(f"Health check complete. Sleeping for {CHECK_INTERVAL_MINUTES} minutes.")
        except Exception as e:
            logging.exception(f"Error during health check: {e}")
        time.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    start_scheduler()
