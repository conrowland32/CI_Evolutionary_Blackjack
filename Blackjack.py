import sys
import multiprocessing
import time
import random as rand
from itertools import product
from Player import Player
from Shoe import Shoe


POPULATION_SIZE = 100
NUMBER_DECKS = 6
HANDS_PER_GENERATION = 2500
NUMBER_GENERATIONS = 200
MUTATION_RATE = 0.1


def worker(decision_table=None, split_table=None):
    shoe = Shoe(NUMBER_DECKS)
    player = Player(decision_table, split_table)
    finish_amount = player.play(shoe, HANDS_PER_GENERATION)
    # print(finish_amount)
    return finish_amount


def mutate(population):
    for i in range(0, len(population), 2):
        individual = population[i]
        for key in individual[0]:
            for i, _ in enumerate(individual[0][key]):
                if rand.random() < MUTATION_RATE:
                    individual[0][key][i] = rand.choice(
                        ["S", "H", "DS", "DH"])
        for key in individual[1]:
            for i, _ in enumerate(individual[1][key]):
                if rand.random() < MUTATION_RATE:
                    individual[1][key][i] = rand.choice(["P", "D"])


if __name__ == "__main__":
    # Initialize starting decision tables
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

        new_population.append((start_decision_table, start_split_table))

    # Spawn and run processes for generation
    with multiprocessing.Pool(POPULATION_SIZE) as pool:
        fitness_scores = pool.starmap(worker, new_population)

    test_table = new_population[0]
    print('Generation 1:', str(sum(fitness_scores) / len(fitness_scores)))

    # Run more generations
    for gen in range(2, NUMBER_GENERATIONS+1):
        # Get the top half of the population
        survivors = sorted(fitness_scores, reverse=True)[
            :int(POPULATION_SIZE/2)]
        survivor_indices = []
        for individual in survivors:
            occurences = [i for i, x in enumerate(
                fitness_scores) if x == individual]
            if len(occurences) > 1:
                for ind in occurences:
                    if ind not in survivor_indices:
                        survivor_indices.append(ind)
            else:
                survivor_indices.append(occurences[0])

        # Create new population
        new_population = [new_population[x]
                          for x in survivor_indices for _ in range(2)]
        mutate(new_population)

        with multiprocessing.Pool(POPULATION_SIZE) as pool:
            fitness_scores = pool.starmap(worker, new_population)
        print('Generation ' + str(gen) + ': ' +
              str(sum(fitness_scores) / len(fitness_scores)))
        if gen % 10 == 0:
            print(new_population)

    sys.exit()
