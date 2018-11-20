import random as rand
import CardHelpers as ch

CARDS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
         "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

BET_VALUE = 2

# Decisions
"""
Normal decisions: 17h/8s
S  -> Stand
H  -> Hit
DH -> Double if allowed, otherwise hit
DS -> Double if allowed, otherwise stand

Split table decisions: 10
P  -> Split
D  -> Default (to normal value)
"""


class Player:
    def __init__(self, decision_table=None, split_table=None):
        self.decision_table = decision_table
        self.split_table = split_table
        self.money = 0.0

    # Play number of hands with given shoe
    def play(self, shoe, num_hands):
        for _ in range(num_hands):
            # Reshuffle shoe every hand -- simulates CSM
            shoe.shuffle()
            new_cards = shoe.deal()
            self.hand1 = [new_cards[0], new_cards[2]]
            self.hand1_bet = BET_VALUE
            self.hand2 = None
            self.hand2_bet = 0
            self.dealer_hand = [new_cards[1], new_cards[3]]

            # Check for dealer blackjack
            if ch.get_raw_value(self.dealer_hand) == 21:
                self.money -= BET_VALUE
                continue

            # Play the hand, and if it is split, play the split hand
            self.play_hand(shoe, self.hand1)
            if self.hand2 is not None:
                self.play_hand(shoe, self.hand2)

            # If hand1 was already a BlackJack, go to next hand
            if self.hand2 is None and len(self.hand1) == 2 and ch.get_raw_value(self.hand1) == 21:
                continue

            # Let the dealer take their turn
            ch.play_dealer(self.dealer_hand, shoe)

            # Check if each hand is a winner and update money accordingly
            if self.hand2 is not None or len(self.hand1) > 2 or ch.get_raw_value(self.hand1) != 21:
                winner = ch.check_winner(self.hand1, self.dealer_hand)
                if winner == 'player':
                    self.money += self.hand1_bet
                elif winner == 'dealer':
                    self.money -= self.hand1_bet
            if self.hand2 is not None:
                winner = ch.check_winner(self.hand2, self.dealer_hand)
                if winner == 'player':
                    self.money += self.hand2_bet
                elif winner == 'dealer':
                    self.money -= self.hand2_bet
        return self.money

    # Play out a given hand using player's strategy
    def play_hand(self, shoe, hand):
        hand_val = ch.get_adjusted_value(hand)
        # Blackjack
        if hand_val == 21:
            self.money += 1.5 * BET_VALUE
            return

        # Play until stand or bust
        while hand_val < 21:
            decision = self.get_decision(hand_val, hand)

            # Stand
            if decision == 'S':
                return
            # Hit
            elif decision == 'H':
                self.hit(hand, shoe)
            # Double if possible, otherwise stand
            elif decision == 'DS':
                if len(hand) == 2:
                    if hand is self.hand1:
                        self.hand1_bet *= 2
                    else:
                        self.hand2_bet *= 2
                    self.hit(hand, shoe)
                    return
                else:
                    return
            # Double if possible, otherwise hit
            elif decision == 'DH':
                if len(hand) == 2:
                    if hand is self.hand1:
                        self.hand1_bet *= 2
                    else:
                        self.hand2_bet *= 2
                    self.hit(hand, shoe)
                    return
                else:
                    self.hit(hand, shoe)
            # Split
            elif decision == 'P':
                self.hand2 = [self.hand1.pop()]
                self.hand2_bet = BET_VALUE
                self.hit(self.hand1, shoe)
                self.hit(self.hand2, shoe)

            # Update hand value
            hand_val = ch.get_adjusted_value(hand)

    # Lookup a table decision based on hand
    def get_decision(self, hand_val, hand):
        # Check if we can split
        dealer_upcard = CARDS[self.dealer_hand[1]]
        if len(hand) == 2 and hand[0] == hand[1]:
            if hand[0] == 'Ace':
                hand_string = 'A'
            else:
                hand_string = str(CARDS[hand[0]])
            decision = self.split_table[hand_string][dealer_upcard-2]
            if decision == 'P' and self.hand2 is None:
                return decision

        # If we can't split, or don't want to
        if ch.is_soft(hand):
            hand_string = "S" + str(hand_val)
        else:
            hand_string = "H" + str(hand_val)
        return self.decision_table[hand_string][dealer_upcard-2]

    # Hit (get new card)
    def hit(self, hand, shoe):
        hand.append(shoe.hit())
