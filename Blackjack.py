import sys
import multiprocessing
import random as rand
# import matplotlib.pyplot as plt
from Player import Player
from Shoe import Shoe


POPULATION_SIZE = 60
NUMBER_DECKS = 4
HANDS_PER_GENERATION = 1000
NUMBER_GENERATIONS = 20
MUTATION_RATE = 0.04


# Worker that creates a new shoe, new player with the given decision tables,
#  and play the new player
def worker(decision_table=None, split_table=None, gen=0):
    shoe = Shoe(NUMBER_DECKS)
    player = Player(decision_table, split_table, gen)
    finish = player.play(shoe, HANDS_PER_GENERATION)
    return finish


# Simple function to mutate every other individual in population based on rate
def mutate(population, rate):
    for i in range(0, len(population), 2):
        individual = population[i]
        for key in individual[0]:
            for i, _ in enumerate(individual[0][key]):
                for x in range(4):
                    if rand.random() < rate:
                        individual[0][key][i][x] = rand.random()
        for key in individual[1]:
            for i, _ in enumerate(individual[1][key]):
                for x in range(2):
                    if rand.random() < rate:
                        individual[1][key][i][x] = rand.random()


if __name__ == "__main__":
    # Lists for graphing
    average_scores = []
    best_scores = []

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
                stops = [rand.random() for _ in range(3)]
                stops.sort()
                start_decision_table[hand].append(
                    [stops[0], stops[1]-stops[0], stops[2]-stops[1], 1-stops[2]])
                # start_decision_table[hand].append(
                #     rand.choice(["S", "H", "DS", "DH"]))

        for hand in start_split_table:
            for _ in range(10):
                stop = rand.random()
                start_split_table[hand].append([stop, 1-stop])
                # start_split_table[hand].append(rand.choice(["P", "D"]))

        new_population.append((start_decision_table, start_split_table))

    # Run generations
    for gen in range(NUMBER_GENERATIONS):
        # Spawn and run player processes
        for ind, individual in enumerate(new_population):
            new_population[ind] = individual + (gen,)

        with multiprocessing.Pool(POPULATION_SIZE) as pool:
            worker_return = pool.starmap(worker, new_population)
        print('Generation ' + str(gen+1) + ': ' +
              str(sum([x[2] for x in worker_return]) / len([x[2] for x in worker_return])) +
              '  (best: ' + str(max([x[2] for x in worker_return])) + ')')
        average_scores.append(
            sum([x[2] for x in worker_return]) / len([x[2] for x in worker_return]))
        best_scores.append(max([x[2] for x in worker_return]))

        # Sort player returns by performance
        worker_return.sort(key=lambda tup: tup[2], reverse=True)
        survivors = worker_return[:int(POPULATION_SIZE/2)]

        # Create new population and mutate some
        new_population = [(x[0], x[1]) for x in survivors for _ in range(2)]
        new_rate = MUTATION_RATE - \
            ((MUTATION_RATE / NUMBER_GENERATIONS) * gen)
        mutate(new_population, new_rate)

    average_file = open("test/average.txt", 'w')
    for score in average_scores:
        average_file.write(str(score) + '\n')
    average_file.close()

    best_file = open("test/best.txt", 'w')
    for score in best_scores:
        best_file.write(str(score) + '\n')
    best_file.close()

    # print(new_population[0])
    sys.exit()
