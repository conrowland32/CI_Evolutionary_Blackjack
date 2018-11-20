import sys
import numpy as np
from Player import Player
from Shoe import Shoe


POPULATION_SIZE = 60
NUMBER_DECKS = 6
HANDS_PER_GENERATION = 1000
NUMBER_GENERATIONS = 1000


if __name__ == "__main__":
    shoe = Shoe(NUMBER_DECKS)
    player1 = Player()
    player1.play(shoe, HANDS_PER_GENERATION)

    sys.exit()
