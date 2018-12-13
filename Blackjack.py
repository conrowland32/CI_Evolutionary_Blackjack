import sys
import multiprocessing
import random as rand
from Player import Player
from Shoe import Shoe
from sklearn.neural_network import MLPClassifier
import CardHelpers as ch

CARDS = {"Two": 2., "Three": 3., "Four": 4., "Five": 5., "Six": 6., "Seven": 7.,
         "Eight": 8., "Nine": 9., "Ten": 10., "Jack": 10., "Queen": 10., "King": 10., "Ace": 11.}

POPULATION_SIZE = 60
NUMBER_DECKS = 4
HANDS_PER_GENERATION = 1000
NUMBER_GENERATIONS = 100

# Worker that creates a new shoe, new player with the given decision tables,
#  and play the new player
def worker(first_network=None, second_network=None, third_network=None):
    """
    This function creates workers that can be run in parallel. Each worker
    should create and run a new player. The parameters should be replaced with
    whatever structure you are using to make player decisions (decision tables,
    neural networks, etc.).
    """
    shoe = Shoe(NUMBER_DECKS)
    player = Player(first_network, second_network, third_network)
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
    average_scores = []
    best_scores = []

    first_network_X = []
    first_network_y = []
    second_network_X = []
    second_network_y = []
    third_network_X = []
    third_network_y = []

    for hand in CARDS:
        for hand2 in CARDS:
            for dealer_upcard in CARDS.values():
                expected_y = ''
                hand_val = CARDS[hand] + CARDS[hand2] 

                if hand == hand2:
                    if hand == 'Ace' or hand == 'Eight':
                        expected_y = 'P'
                    elif hand == 'Two' or hand == 'Three' or hand == 'Seven':
                        if dealer_upcard < 8:
                            expected_y = 'P'
                        else:
                            expected_y = 'H'
                    elif hand == 'Four':
                        if dealer_upcard == 5 or dealer_upcard == 6:
                            expected_y = 'P'
                        else:
                            expected_y = 'H'
                    elif hand == 'Six':
                        if dealer_upcard < 7:
                            expected_y = 'P'
                        else:
                            expected_y = 'H'
                    elif hand == 'Nine':
                        if dealer_upcard in [7, 10, 11]:
                            expected_y = 'S'
                        else:
                            expected_y = 'P'

                first_network_X.append([CARDS[hand], CARDS[hand2], dealer_upcard])
                first_network_y.append(1 if expected_y == 'P' else 0)

                if not ch.is_soft([hand, hand2]):
                    if hand_val < 9:
                        expected_y = 'H'
                    elif hand_val == 9:
                        if dealer_upcard == 2 or dealer_upcard > 6:
                            expected_y = 'H'
                        else:
                            expected_y = 'D'
                    elif hand_val == 10:
                        if dealer_upcard < 10:
                            expected_y = 'D'
                        else:
                            expected_y = 'H'
                    elif hand_val == 11:
                        expected_y = 'D'
                    elif hand_val == 12:
                        if dealer_upcard < 4 or dealer_upcard > 6:
                            expected_y = 'H'
                        else:
                            expected_y = 'S'
                    elif hand_val > 12 and hand_val < 17:
                        if dealer_upcard < 7:
                            expected_y = 'S'
                        else:
                            expected_y = 'H'
                    elif hand_val > 16:
                        expected_y = 'S'
                else:
                    if hand_val == 12:
                        expected_y = 'H'
                    if hand_val == 13 or hand_val == 14:
                        if dealer_upcard == 5 or dealer_upcard == 6:
                            expected_y = 'D'
                        else:
                            expected_y = 'H'
                    if hand_val == 15 or hand_val == 16:
                        if dealer_upcard < 4 or dealer_upcard > 6:
                            expected_y = 'H'
                        else:
                            expected_y = 'D'
                    if hand_val == 17:
                        if dealer_upcard == 2 or dealer_upcard > 6:
                            expected_y = 'H'
                        else:
                            expected_y = 'D'
                    if hand_val == 18:
                        if dealer_upcard < 7:
                            expected_y = 'D'
                        if dealer_upcard < 9:
                            expected_y = 'S'
                        else:
                            expected_y = 'H'
                    if hand_val == 19:
                        if dealer_upcard == 6:
                            expected_y = 'D'
                        else:
                            expected_y = 'S'
                    if hand_val > 19:
                        expected_y = 'S'

                second_network_X.append([CARDS[hand], CARDS[hand2], dealer_upcard])

                temp = [0]*16
                temp[0] = CARDS[hand]
                temp[1] = CARDS[hand]
                temp[-1] = dealer_upcard
                third_network_X.append(temp)

                if expected_y == 'D':
                    second_network_y.append(1)
                    third_network_y.append(0)
                else:
                    second_network_y.append(0)
                    third_network_y.append(1 if expected_y == 'H' else 0)

    for count in range(POPULATION_SIZE):
        first_network = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(1), random_state=1), first_network_X, first_network_y]
        second_network = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(1), random_state=1), second_network_X, second_network_y]
        third_network = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5), random_state=1), third_network_X, third_network_y]
       
        first_network[0].fit(first_network[1], first_network[2])
        second_network[0].fit(second_network[1], second_network[2])
        third_network[0].fit(third_network[1], third_network[2])

        """
        Be sure to append all needed structures to new_population as a tuple
        when you are done; this is what will be passed to workers as
        parameters.
        """
        new_population.append((first_network, second_network, third_network))

    # Run generations
    for gen in range(NUMBER_GENERATIONS):
        # Spawn and run player processes
        with multiprocessing.Pool(POPULATION_SIZE) as pool:
            worker_return = pool.starmap(worker, new_population)
        print('Generation ' + str(gen+1) + ': ' +
              str(sum([x[0] for x in worker_return]) / len([x[0] for x in worker_return])) +
              '  (best: ' + str(max([x[0] for x in worker_return])) + ')')

        average_scores.append(sum([x[0] for x in worker_return]) / len([x[0] for x in worker_return]))
        best_scores.append(max([x[0] for x in worker_return]))

        """
        Now that all the workers have been run, fitness_scores should contain
        the total money won or lost by each player. This is where you should
        add the additional learning for your solution: backpropogation,
        mutation, crossover, etc. When you are done with this step, be sure to
        create the new population and store it in new_population the same as
        before.
        """
        
        new_population = []
        for x in worker_return:
            first_network = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(1), random_state=1), x[1][1], x[1][2]]
            second_network = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(1), random_state=1), x[2][1], x[2][2]]
            third_network = [MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5), random_state=1), x[3][1], x[3][2]]
			
			
            
			if(len(new_population) > 10):
				randNum = rand.random() * len(new_population)
				first_network = new_population[randNum][0]
				randNum = rand.random() * len(new_population)
				second_network = new_population[randNum][1]
				randNum = rand.random() * len(new_population)
				third_network = new_population[randNum][2]
			else: 
				first_network[0].fit(first_network[1], first_network[2])
				second_network[0].fit(second_network[1], second_network[2])
				third_network[0].fit(third_network[1], third_network[2])
			
            new_population.append((first_network, second_network, third_network))

    average_file = open("data/average.txt", 'w')
    for score in average_scores:
        average_file.write(str(score) + '\n')
    average_file.close()

    best_file = open("data/best.txt", 'w')
    for score in best_scores:
        best_file.write(str(score) + '\n')
    best_file.close()


    # print(new_population[0])
    sys.exit()