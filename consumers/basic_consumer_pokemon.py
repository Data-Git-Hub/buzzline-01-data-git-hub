"""
basic_consumer_pokemon.py

Custom consumer that tails the project log and performs lightweight real-time analytics:
- Rolling average of payload length (characters) Add 1
- Keyword/pattern alerts for selected events (e.g., "Hyper Beam", "evolved") Add 2
"""

# Standard library
import os
import time
import re
from collections import deque
from typing import Deque

# Local
from utils.utils_logger import logger, get_log_file_path


def extract_payload(log_line: str) -> str:
    """
    Extract the message payload after the ' - ' separator inserted by loguru.
    If the separator is not found, return the whole line.
    """
    sep = " - "
    idx = log_line.find(sep)
    return log_line[idx + len(sep):] if idx != -1 else log_line


def process_stream(log_file: str, window_size: int = 20, report_every: int = 5) -> None:
    """
    Tail the log file and run simple analytics.

    Args:
        log_file: path to the log file to follow
        window_size: number of recent messages for rolling average
        report_every: print the average every N messages
    """
    window: Deque[int] = deque(maxlen=window_size)
    count = 0

    # --- Keyword/Pattern Alerts ---
    # Case-insensitive, tolerant of "HyperBeam" vs "Hyper Beam"
    KEYWORD_PATTERNS = [
        re.compile(r"\bhyper\s*beam\b", re.IGNORECASE),
        re.compile(r"\bevolved\b", re.IGNORECASE),
    ]

    with open(log_file, "r", encoding="utf-8") as f:
        # Seek to the end and wait for new lines
        f.seek(0, os.SEEK_END)
        print(f"Consumer ready. Tailing {log_file} ...")

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            raw = line.strip()
            if not raw:
                continue

            # Extract the payload and compute length
            payload = extract_payload(raw)
            length = len(payload)
            window.append(length)
            count += 1

            print(f"Consumed: {payload}")

            # --- Keyword alerts ---
            if any(p.search(payload) for p in KEYWORD_PATTERNS):
                alert = f"ALERT (keyword): {payload}"
                print(alert)
                logger.warning(alert)

            # --- Rolling average report ---
            if count % report_every == 0:
                avg = sum(window) / len(window)
                msg = f"Rolling avg payload length (last {len(window)}): {avg:.1f} chars"
                print(msg)
                logger.info(msg)


def main() -> None:
    logger.info("START basic_consumer_pokemon...")

    log_file_path = get_log_file_path()
    logger.info(f"Reading file located at {log_file_path}.")

    try:
        process_stream(str(log_file_path), window_size=20, report_every=5)
    except KeyboardInterrupt:
        print("User stopped the consumer (CTRL+C).")
    finally:
        logger.info("END basic_consumer_pokemon.")


if __name__ == "__main__":
    main()
