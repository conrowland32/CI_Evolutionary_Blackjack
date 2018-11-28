import sys
import multiprocessing
import random as rand
from Player import Player
from Shoe import Shoe


POPULATION_SIZE = 100
NUMBER_DECKS = 4
HANDS_PER_GENERATION = 1000
NUMBER_GENERATIONS = 1000
MUTATION_RATE = 0.01


# Worker that creates a new shoe, new player with the given decision tables,
#  and play the new player
def worker(decision_table=None, split_table=None):
    """
    This function creates workers that can be run in parallel. Each worker
    should create and run a new player. The parameters should be replaced with
    whatever structure you are using to make player decisions (decision tables,
    neural networks, etc.).
    """
    shoe = Shoe(NUMBER_DECKS)
    player = Player(decision_table, split_table)
    finish_amount = player.play(shoe, HANDS_PER_GENERATION)
    return finish_amount


if __name__ == "__main__":
    # Initialize starting player strategy structures
    """
    First, initialize the structure you are using to represent player strategy.
    The example below creates random decision tables, but this is also where
    you should create random new neural networks, etc.
    """
    new_population = []
    for _ in range(POPULATION_SIZE):
        start_decision_table = {
            "H4": [], "H5": [], "H6": [], "H7": [], "H8": [],
            "H9": [], "H10": [], "H11": [], "H12": [], "H13": [],
            "H14": [], "H15": [], "H16": [], "H17": [], "H18": [],
            "H19": [], "H20": [], "S12": [], "S13": [], "S14": [],
            "S15": [], "S16": [], "S17": [], "S18": [], "S19": [], "S20": []
        }
        start_split_table = {
            "2": [], "3": [], "4": [], "5": [], "6": [],
            "7": [], "8": [], "9": [], "10": [], "A": []
        }

        for hand in start_decision_table:
            for _ in range(10):
                start_decision_table[hand].append(
                    rand.choice(["S", "H", "DS", "DH"]))

        for hand in start_split_table:
            for _ in range(10):
                start_split_table[hand].append(rand.choice(["P", "D"]))

        """
        Be sure to append all needed structures to new_population as a tuple
        when you are done; this is what will be passed to workers as
        parameters.
        """
        new_population.append((start_decision_table, start_split_table))

    # Run generations
    for gen in range(NUMBER_GENERATIONS):
        # Spawn and run player processes
        with multiprocessing.Pool(POPULATION_SIZE) as pool:
            fitness_scores = pool.starmap(worker, new_population)
        print('Generation ' + str(gen+1) + ': ' +
              str(sum(fitness_scores) / len(fitness_scores)))

        """
        Now that all the workers have been run, fitness_scores should contain
        the total money won or lost by each player. This is where you should
        add the additional learning for your solution: backpropogation,
        mutation, crossover, etc. When you are done with this step, be sure to
        create the new population and store it in new_population the same as
        before.
        """

    print(new_population[0])
    sys.exit()
