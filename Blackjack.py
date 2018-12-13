import sys
import multiprocessing
import random as rand
from Norm_Player import Player
from Fuzzy_Player import FPlayer
from Super_Fuzzy_Player import S_FPlayer
from Shoe import Shoe
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

NUM_DECKS = 6
NUM_HANDS = 50

shoe = Shoe(NUM_DECKS)

# Worker functions create the player and play the game with given shoe and number of hands
def worker(decision_table=None, split_table=None):
    shoe_norm = copy.deepcopy(shoe)
    player = Player(decision_table, split_table)
    finish_amount = player.play(shoe_norm, NUM_HANDS)
    return finish_amount

def f_worker(decision_table=None, split_table=None):
    shoe_fuzzy = copy.deepcopy(shoe)
    fplayer = FPlayer(decision_table, split_table)
    finish_amount = fplayer.play(shoe_fuzzy, NUM_HANDS)
    return finish_amount

def s_f_worker(decision_table=None, split_table=None):
    shoe_s_fuzzy = copy.deepcopy(shoe)
    s_fplayer = S_FPlayer(decision_table, split_table)
    finish_amount = s_fplayer.play(shoe_s_fuzzy, NUM_HANDS)
    return finish_amount


if __name__ == "__main__":
    # Initialize starting decision tables
    
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

    decision_table2 = copy.deepcopy(start_decision_table)
    split_table2 = copy.deepcopy(start_split_table)  
    decision_table3 = copy.deepcopy(start_decision_table)
    split_table3 = copy.deepcopy(start_split_table) 

    i = 0
    net_norm = 0
    net_fuzz = 0
    net_sfuzz = 0
    while i < 100:
        #print(worker(start_decision_table, start_split_table))
        #print(f_worker(decision_table2, split_table2))
        data1 = plt.plot(i, worker(start_decision_table, start_split_table), color = "blue", marker = ".", label = 'Normal')
        data2 = plt.plot(i, f_worker(decision_table2, split_table2), color = "green", marker = ".", label = 'Fuzzy')
        data3 = plt.plot(i, s_f_worker(decision_table3, split_table3), color = "red", marker = ".", label = 'Super Fuzzy')
        net_norm += worker(start_decision_table, start_split_table)
        net_fuzz += f_worker(decision_table2, split_table2)
        net_sfuzz += s_f_worker(decision_table3, split_table3)
        shoe.shuffle()
        i = i + 1    

    print(net_norm)
    print(net_fuzz)
    print(net_sfuzz)
    net1 = net_norm/100
    net2 = net_fuzz/100
    net3 = net_sfuzz/100
    print(net1)
    print(net2)
    print(net3)
    plt.xlabel("Round")
    plt.ylabel("Total Player Money")
    plt.title("Normal Player vs. Fuzzy Player in Blackjack")
    blue = mpatches.Patch(color = 'blue', label = 'Normal')
    green = mpatches.Patch(color = 'green', label = 'Fuzzy')
    red = mpatches.Patch(color = 'red', label = 'Super Fuzzy')
    plt.legend(loc = 'upper right')
    plt.legend(handles = [blue, green, red])
    plt.show()
    sys.exit()
