import random as rand
import CardHelpers as ch
import copy

CARDS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
         "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

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


class S_FPlayer:
    def __init__(self, decision_table=None, split_table=None):
        self.decision_table = decision_table
        self.split_table = split_table
        self.money = 10000.0

    def get_count(self, cards, count):
        # Updates card count from the cards that are dealt
        
        if cards[0] == 'Two' or cards[0] == 'Three' or cards[0] == 'Four' \
        or cards[0] == 'Five' or cards[0] == 'Six' or cards[0] == "Seven":
            count += 1
        if cards[1] == 'Two' or cards[1] == 'Three' or cards[1] == 'Four' \
        or cards[1] == 'Five' or cards[1] == 'Six' or cards[1] == "Seven":
            count += 1
        if cards[2] == 'Two' or cards[2] == 'Three' or cards[2] == 'Four' \
        or cards[2] == 'Five' or cards[2] == 'Six' or cards[2] == "Seven":
            count += 1
        if cards[3] == 'Two' or cards[3] == 'Three' or cards[3] == 'Four' \
        or cards[3] == 'Five' or cards[3] == 'Six' or cards[3] == "Seven":
            count += 1

        if cards[0] == 'Ten' or cards[0] == 'Jack' or cards[0] == 'Queen' \
        or cards[0] == 'King' or cards[0] == 'Ace':
            count -= 1
        if cards[1] == 'Ten' or cards[1] == 'Jack' or cards[1] == 'Queen' \
        or cards[1] == 'King' or cards[1] == 'Ace':
            count -= 1
        if cards[2] == 'Ten' or cards[2] == 'Jack' or cards[2] == 'Queen' \
        or cards[2] == 'King' or cards[2] == 'Ace':
            count -= 1
        if cards[3] == 'Ten' or cards[3] == 'Jack' or cards[3] == 'Queen' \
        or cards[3] == 'King' or cards[3] == 'Ace':
            count -= 1

        return count

    # Fuzzy logic with triangular membership functions to determine betting amount based off count
    def make_bet(self, count):
        bet = 0
        if count <= -16:
            bet = 2
        if count > -16 and count < -12:
            bet = ((count + 10)/(-16 + 10))*50
        if count >= -12 and count <= -10:
            bet1 = ((count + 10)/(-16 + 10))*75
            bet2 = ((count + 12)/(-6 + 12))*75
            if bet1 > bet2:
                bet = bet1
            else:
                bet = bet2 
        if count > -10 and count < -6: 
            bet = ((count+12)/(-6+12))*100
        if count == -6:
            bet = 125
        if count > -6 and count < -2:
            bet = ((count+0)/(-6 + 0))*150    
        if count >= -2 and count <= 0:
            bet1 = ((count + 0)/(-6 + 0))*175
            bet2 = ((count + 2)/(4 + 2))*175
            if bet1 > bet2:
                bet = bet1
            else:
                bet = bet2 
        if count > 0 and count < 4:
            bet = ((count + 2)/(4 + 2))*200
        if count == 4:
            bet = 225
        if count > 4 and count < 8:
            bet = ((count - 10)/(4 - 10))*250
        if count >= 8 and count <= 10:
            bet1 = ((count - 10)/(4 - 10))*275
            bet2 = ((count -8)/(14 - 8))*275
            if bet1 > bet2:
                bet = bet1
            else:
                bet = bet2 
        if count > 10 and count < 14:
            bet = ((count - 8)/(14 - 8))*300
        if count == 14:
            bet = 325
        if count > 14 and count < 18:
            bet = ((count - 20)/(14 - 20))*350
        if count >= 18 and count <= 20:
            bet1 = ((count - 20)/(14 - 20))*375
            bet2 = ((count - 18)/(24 - 18))*375
            if bet1 > bet2:
                bet = bet1
            else:
                bet = bet2 
        if count > 20 and count < 24:
            bet = ((count - 18)/(24 - 18))*425
        if count >= 24:
            bet = 500

        if bet < 2:
            bet = 2

        return bet

    # Play number of hands with given shoe
    def play(self, shoe, num_hands):
    
        # KO card counting method starts count at -20 with 6 decks in shoe
        card_count = -20

        for _ in range(num_hands):

            new_cards = shoe.deal()
            card_count = self.get_count(new_cards, card_count)
            #print(card_count)
            self.hand1 = [new_cards[0], new_cards[2]]
            self.hand1_bet = self.make_bet(card_count)
            self.hand2 = None
            self.hand2_bet = 0
            self.dealer_hand = [new_cards[1], new_cards[3]]

            # Check for dealer blackjack
            if ch.get_raw_value(self.dealer_hand) == 21:
                self.money -= self.hand1_bet
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
            self.money += 1.5 * self.hand1_bet
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
                self.hand2_bet = self.hand1_bet
                self.hand1.append(shoe.hit())
                self.hand2.append(shoe.hit())

            # Update hand value
            hand_val = ch.get_adjusted_value(hand)

    # Get the decision the player will make based on basic blackjack strategy
    def get_decision(self, hand_val, hand):
        
        x = 0
        y = 0
        z = 0

        dealer_upcard = CARDS[self.dealer_hand[1]]
        # Could not use fuzzy logic for when the player should split. This is the most optimal way
        #   to play that type of hand.
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

        # Fuzzy logic implementations for when the player's hand is not soft (no ace)
        if not ch.is_soft(hand):

            if hand_val < 9:
                return 'H'

            if hand_val == 9:
                x = 1
                if dealer_upcard == 2:
                    y = 1
                if dealer_upcard > 6:
                    if dealer_upcard < 7:
                        z = (dealer_upcard - 5)/(7 - 5)
                    if dealer_upcard > 7 and dealer_upcard < 10:
                        z = (dealer_upcard - 10)/(7 - 10)
                    if dealer_upcard > 9:
                        z = 1
                    if y > z:
                        return 'H'
                    elif z >= y:
                        if x <= z:
                            return 'H'
                        elif x > z:
                            return 'DH'            
                else:
                    return 'H'
            

            x = 0
            y = 0
            z = 0

            if hand_val == 10:
                x = 1
                if dealer_upcard < 10:
                    if dealer_upcard < 2:
                        y = 1
                    if dealer_upcard > 2 and dealer_upcard < 4:
                        y = (dealer_upcard - 2)/(4 - 2)
                    if dealer_upcard == 4:
                        y = 1
                    if dealer_upcard > 4 and dealer_upcard < 6:
                        y = (dealer_upcard - 6)/(4 - 6)
                    if dealer_upcard == 7:
                        y = 1
                    if dealer_upcard > 7 and dealer_upcard < 10:
                        y = (dealer_upcard - 10)/(7 - 10)
                    if x == y:
                        return 'DH'
                    elif x != y:
                        return 'H'
                else:
                    return 'H'
            

            x = 0
            y = 0
            z = 0

            if hand_val == 11:
                return 'DH'

            if hand_val == 12:
                x = 1
                if dealer_upcard < 4:
                    y = (dealer_upcard - 2)/(4 - 2)
                elif dealer_upcard > 6:
                    if dealer_upcard == 7:
                        z = 1
                    elif dealer_upcard > 7 and dealer_upcard < 10:
                        z = (dealer_upcard - 10)/(7 - 10)
                    elif dealer_upcard > 10:
                        z = 1
                else:
                    return 'S'
                if y > z:
                    if y < x:
                        return 'H'
                else:
                    return 'S'

            x = 0
            y = 0
            z = 0
                   
            if hand_val > 12 and hand_val < 17:
                if hand_val > 12 and hand_val < 14:
                    x = (hand_val - 12)/(14 - 12)
                elif hand_val == 14:
                    x = 1
                elif hand_val > 14 and hand_val < 16:
                    x = (hand_val - 16)/(14 - 16)
                else:
                    x = 1 
                if dealer_upcard < 7:
                    if dealer_upcard == 6:
                        y = (dealer_upcard - 5)/(7 - 5)
                    if dealer_upcard == 5:
                        y = (dealer_upcard - 6)/(4 - 6)
                    if dealer_upcard == 4:
                        y = 1
                    if dealer_upcard == 3:
                        y = (dealer_upcard - 2)/(4 - 2)
                    if dealer_upcard < 3:
                        y = 1
                if x > y:
                    return 'H'
                else:
                    return 'S'

            x = 0 
            y = 0
            z = 0

            if hand_val > 16:
                return 'S'

        # Fuzzy logic implementations for when the player's hand is soft (has an ace)
        if ch.is_soft(hand):

            if hand_val == 12:
                return 'H'

            if hand_val == 13 or hand_val == 14:
                if dealer_upcard == 5 or dealer_upcard == 6:
                    return 'DH'
                else:
                    return 'H'
            

            if hand_val == 15 or hand_val == 16:
                x = 1
                if dealer_upcard < 4:
                    y = (dealer_upcard - 2)/(4 - 2)
                if dealer_upcard > 6:
                    if dealer_upcard == 7:
                        z = 1
                    if dealer_upcard > 7 and dealer_upcard < 10:
                        z = (dealer_upcard - 10)/(7 - 10)
                    if dealer_upcard > 10:
                        z = 1
                else:
                    return 'S'
                if y > z:
                    if y < x:
                        return 'H'
                    else:
                        return 'S'
                else:
                    return 'S'
            

            x = 0
            y = 0
            z = 0

            if hand_val == 17:
                x = 1
                if dealer_upcard == 2:
                    y = 1
                if dealer_upcard > 6:
                    if dealer_upcard < 7:
                        z = (dealer_upcard - 5)/(7 - 5)
                    if dealer_upcard > 7 and dealer_upcard < 10:
                        z = (dealer_upcard - 10)/(7 - 10)
                    if dealer_upcard > 9:
                        z = 1
                if y > z:
                    return 'H'
                elif z > y:
                    if x <= z:
                        return 'H'
                    elif x > z:
                        return 'DH'
                else:
                    return "H"
            

            x = 0
            y = 0
            z = 0

            if hand_val == 18:
                x = 1
                if dealer_upcard < 9 and dealer_upcard > 7:
                    z = (dealer_upcard - 10)/(7 - 10)
                if dealer_upcard == 7:
                    z = 1
                if dealer_upcard < 7 and dealer_upcard > 5:
                    y = (dealer_upcard - 5)/(7 - 5)
                if dealer_upcard < 5 and dealer_upcard > 4:
                    y = (dealer_upcard - 6)/(4 - 6)
                if dealer_upcard == 4:
                    y = 1
                if dealer_upcard < 4 and dealer_upcard > 2:
                    y = (dealer_upcard - 2)/(4 - 2)
                if dealer_upcard == 2:
                    y = 1
                if y > z:
                    if x > y:
                        return 'DS'
                    else:
                        return 'S'
                elif z > y:
                    if x > y:
                        return 'S'
                    else:
                        return 'DS' 
                else:
                    return 'H'


            x = 0
            y = 0
            z = 0

            if hand_val == 19:
                if dealer_upcard == 6:
                    return 'DS'
                else:
                    return 'S'

            if hand_val > 19:
                return 'S'
        else:
            return 'H'

