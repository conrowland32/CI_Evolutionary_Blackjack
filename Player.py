import random as rand
import CardHelpers as ch

CARDS = {"Two": 2., "Three": 3., "Four": 4., "Five": 5., "Six": 6., "Seven": 7.,
         "Eight": 8., "Nine": 9., "Ten": 10., "Jack": 10., "Queen": 10., "King": 10., "Ace": 11.}

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
    def __init__(self, first_network=None, second_network=None, third_network=None):
        self.first_network = first_network
        self.second_network = second_network
        self.third_network = third_network
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
        return [self.money, self.first_network, self.second_network, self.third_network]

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
        expected_y = ''

        dealer_upcard = CARDS[self.dealer_hand[1]]
        if len(hand) == 2 and hand[0] == hand[1] and hand is self.hand1:
            if hand[0] == 'Ace' or hand[0] == 'Eight':
                expected_y = 'P'
            if hand[0] == 'Two' or hand[0] == 'Three' or hand[0] == 'Seven':
                if dealer_upcard < 8:
                    expected_y = 'P'
                else:
                    expected_y = 'H'
            if hand[0] == 'Four':
                if dealer_upcard == 5 or dealer_upcard == 6:
                    expected_y = 'P'
                else:
                    expected_y = 'H'
            if hand[0] == 'Six':
                if dealer_upcard < 7:
                    expected_y = 'P'
                else:
                    expected_y = 'H'
            if hand[0] == 'Nine':
                if dealer_upcard in [7, 10, 11]:
                    expected_y = 'S'
                else:
                    expected_y = 'P'

        if not ch.is_soft(hand):
            if hand_val < 9:
                expected_y = 'H'
            if hand_val == 9:
                if dealer_upcard == 2 or dealer_upcard > 6:
                    expected_y = 'H'
                else:
                    expected_y = 'DH'
            if hand_val == 10:
                if dealer_upcard < 10:
                    expected_y = 'DH'
                else:
                    expected_y = 'H'
            if hand_val == 11:
                expected_y = 'DH'
            if hand_val == 12:
                if dealer_upcard < 4 or dealer_upcard > 6:
                    expected_y = 'H'
                else:
                    expected_y = 'S'
            if hand_val > 12 and hand_val < 17:
                if dealer_upcard < 7:
                    expected_y = 'S'
                else:
                    expected_y = 'H'
            if hand_val > 16:
                expected_y = 'S'

        if ch.is_soft(hand):
            if hand_val == 12:
                expected_y = 'H'
            if hand_val == 13 or hand_val == 14:
                if dealer_upcard == 5 or dealer_upcard == 6:
                    expected_y = 'DH'
                else:
                    expected_y = 'H'
            if hand_val == 15 or hand_val == 16:
                if dealer_upcard < 4 or dealer_upcard > 6:
                    expected_y = 'H'
                else:
                    expected_y = 'DH'
            if hand_val == 17:
                if dealer_upcard == 2 or dealer_upcard > 6:
                    expected_y = 'H'
                else:
                    expected_y = 'DH'
            if hand_val == 18:
                if dealer_upcard < 7:
                    expected_y = 'DS'
                if dealer_upcard < 9:
                    expected_y = 'S'
                else:
                    expected_y = 'H'
            if hand_val == 19:
                if dealer_upcard == 6:
                    expected_y = 'DS'
                else:
                    expected_y = 'S'
            if hand_val > 19:
                expected_y = 'S'

        if len(hand) == 2:
            if hand[0] == hand[1] and hand is self.hand1:
                temp = self.first_network[0].predict([[CARDS[hand[0]], CARDS[hand[1]], dealer_upcard]])
                self.first_network[1].append([CARDS[hand[0]], CARDS[hand[1]], dealer_upcard])
                self.first_network[2].append(1 if expected_y == 'P' else 0)
                if temp[0] == 1:
                    return 'P'

            temp = self.second_network[0].predict([[CARDS[hand[0]], CARDS[hand[0]], dealer_upcard]])
            self.second_network[1].append([CARDS[hand[0]], CARDS[hand[1]], dealer_upcard])
            self.second_network[2].append(1 if expected_y in ['DH', 'DS'] else 0)
            if temp[0] == 1:
                return 'DH'

        temp_cards = [CARDS[hand[idx]] if idx < len(hand) else 0 for idx in range(16)]
        temp_cards[-1] = dealer_upcard

        temp = self.third_network[0].predict([temp_cards])
        self.third_network[1].append(temp_cards)
        self.third_network[2].append(1 if expected_y == 'H' else 0)
        if temp[0] == 1:
            return 'H'
        return 'S'

