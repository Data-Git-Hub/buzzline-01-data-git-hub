"""
basic_producer_pokemon.py

Custom producer that emits Pokémon-themed streaming messages.
"""

# Standard library
import os
import random
import time

# External
from dotenv import load_dotenv

# Local
from utils.utils_logger import logger

load_dotenv()


def get_message_interval() -> int:
    """
    Return message interval in seconds from env (MESSAGE_INTERVAL_SECONDS) or default.
    """
    raw = os.getenv("MESSAGE_INTERVAL_SECONDS", "2")
    interval = int(raw)
    logger.info(f"[POKÉMON PRODUCER] Interval = {interval} sec")
    return interval


# Pokémon-themed vocab
POKEMON = [
    "Pikachu", "Charmander", "Bulbasaur", "Squirtle",
    "Eevee", "Snorlax", "Gengar", "Jigglypuff", "Mewtwo"
]
MOVES = [
    "Thunderbolt", "Flamethrower", "Vine Whip", "Water Gun",
    "Quick Attack", "Hyper Beam", "Shadow Ball", "Sing", "Psychic"
]
VERBS = ["encountered", "battled", "caught", "trained", "evolved"]
OUTCOMES = ["epic", "tough", "effortless", "close", "critical", "hilarious"]


def generate_messages():
    """
    Yield one Pokémon-themed message at a time (infinite generator).
    """
    while True:
        mon = random.choice(POKEMON)
        move = random.choice(MOVES)
        verb = random.choice(VERBS)
        outcome = random.choice(OUTCOMES)
        yield f"Trainer {verb} {mon} using {move}. Outcome: {outcome}."


def main() -> None:
    logger.info("START basic_producer_pokemon...")
    logger.info("Press CTRL+C to stop.")

    interval_secs = get_message_interval()

    for message in generate_messages():
        logger.info(message)
        time.sleep(interval_secs)

    logger.info("END basic_producer_pokemon.")


if __name__ == "__main__":
    main()