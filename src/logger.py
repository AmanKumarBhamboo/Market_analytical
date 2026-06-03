import sys
import os
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def log_note(note: str):
    logging.info(note)
    print(f"Log saved to: {LOG_FILE_PATH}")
    print(f"Recorded: {note}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/logger.py <your note>")
        print("   or: python src/logger.py \"note in quotes\"")
        sys.exit(1)

    note = " ".join(sys.argv[1:])
    log_note(note)