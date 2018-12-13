import random as rand

CARDS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
         "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

class Shoe:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.shuffle()

    # Shuffle the deck
    def shuffle(self):
        self.cards = []
        for _ in range(self.num_decks):
            for c in CARDS:
                for _ in range(4):
                    self.cards.append(c)
        rand.shuffle(self.cards)

    # Pop four cards off the shoe for the starting deal
    #  (2 for player, 2 for dealer)
    def deal(self):
        return [self.cards.pop() for _ in range(4)]

    # Pop one card off the shoe and return it
    def hit(self):
        return self.cards.pop()
