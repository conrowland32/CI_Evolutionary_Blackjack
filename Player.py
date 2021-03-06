import random as rand
import CardHelpers as ch

CARDS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
         "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

BET_VALUE = 2

# Decisions
"""
Normal decisions (soft or hard hands):
S  -> Stand
H  -> Hit
DH -> Double if allowed, otherwise hit
DS -> Double if allowed, otherwise stand

Split table decisions (pair of same card):
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
                hand.append(shoe.hit())
            # Double if possible, otherwise stand
            elif decision == 'DS':
                if len(hand) == 2:
                    if hand is self.hand1:
                        self.hand1_bet *= 2
                    else:
                        self.hand2_bet *= 2
                    hand.append(shoe.hit())
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
                    hand.append(shoe.hit())
                    return
                else:
                    hand.append(shoe.hit())
            # Split
            elif decision == 'P':
                self.hand2 = [self.hand1.pop()]
                self.hand2_bet = BET_VALUE
                self.hand1.append(shoe.hit())
                self.hand2.append(shoe.hit())

            # Update hand value
            hand_val = ch.get_adjusted_value(hand)

    # Get the decision the player will make based on their strategy
    def get_decision(self, hand_val, hand):
        """
        This is where you should implement the decision-making for your
        experiment. For example, if you are training neural networks to make
        decisions, this function should take the applicable inputs (player
        hand, dealer hand, etc.) and compute the network output decision.

        The sample provided below is hard-coded basic strategy. The player
        return for this method should be ~99.5%
        """
        dealer_upcard = CARDS[self.dealer_hand[1]]
        if len(hand) == 2 and hand[0] == hand[1] and hand is self.hand1:
            if hand[0] == 'Ace' or hand[0] == 'Eight':
                return 'P'
            if hand[0] == 'Two' or hand[0] == 'Three' or hand[0] == 'Seven':
                if dealer_upcard < 8:
                    return 'P'
                else:
                    return 'H'
            if hand[0] == 'Four':
                if dealer_upcard == 5 or dealer_upcard == 6:
                    return 'P'
                else:
                    return 'H'
            if hand[0] == 'Six':
                if dealer_upcard < 7:
                    return 'P'
                else:
                    return 'H'
            if hand[0] == 'Nine':
                if dealer_upcard in [7, 10, 11]:
                    return 'S'
                else:
                    return 'P'

        if not ch.is_soft(hand):
            if hand_val < 9:
                return 'H'
            if hand_val == 9:
                if dealer_upcard == 2 or dealer_upcard > 6:
                    return 'H'
                else:
                    return 'DH'
            if hand_val == 10:
                if dealer_upcard < 10:
                    return 'DH'
                else:
                    return 'H'
            if hand_val == 11:
                return 'DH'
            if hand_val == 12:
                if dealer_upcard < 4 or dealer_upcard > 6:
                    return 'H'
                else:
                    return 'S'
            if hand_val > 12 and hand_val < 17:
                if dealer_upcard < 7:
                    return 'S'
                else:
                    return 'H'
            if hand_val > 16:
                return 'S'

        if ch.is_soft(hand):
            if hand_val == 12:
                return 'H'
            if hand_val == 13 or hand_val == 14:
                if dealer_upcard == 5 or dealer_upcard == 6:
                    return 'DH'
                else:
                    return 'H'
            if hand_val == 15 or hand_val == 16:
                if dealer_upcard < 4 or dealer_upcard > 6:
                    return 'H'
                else:
                    return 'DH'
            if hand_val == 17:
                if dealer_upcard == 2 or dealer_upcard > 6:
                    return 'H'
                else:
                    return 'DH'
            if hand_val == 18:
                if dealer_upcard < 7:
                    return 'DS'
                if dealer_upcard < 9:
                    return 'S'
                else:
                    return 'H'
            if hand_val == 19:
                if dealer_upcard == 6:
                    return 'DS'
                else:
                    return 'S'
            if hand_val > 19:
                return 'S'
