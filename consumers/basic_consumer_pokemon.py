"""
basic_consumer_pokemon.py

Custom consumer that tails the project log and prints a rolling average
of message payload length (characters) over the last N messages.
"""

# Standard library
import os
import time
from collections import deque
from typing import Deque

# Local
from utils.utils_logger import logger, get_log_file_path


def extract_payload(log_line: str) -> str:
    """
    Extract the message payload after the ' - ' separator inserted by loguru.
    If the separator is not found, return the whole line.
    Example line:
    2025-08-28 ... INFO ... - Trainer battled Pikachu using Thunderbolt. Outcome: epic.
    """
    sep = " - "
    idx = log_line.find(sep)
    return log_line[idx + len(sep):] if idx != -1 else log_line


def process_stream(log_file: str, window_size: int = 20, report_every: int = 5) -> None:
    """
    Tail the log file and report rolling average payload length.

    Args:
        log_file: path to the log file to follow
        window_size: number of recent messages to average over
        report_every: print average every N messages to reduce noise
    """
    window: Deque[int] = deque(maxlen=window_size)
    count = 0

    with open(log_file, "r", encoding="utf-8") as f:
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

            payload = extract_payload(raw)
            length = len(payload)
            window.append(length)
            count += 1

            print(f"Consumed: {payload}")

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
