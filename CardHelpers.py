CARDS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
         "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}


def is_soft(hand):
    if 'Ace' not in hand:
        return False
    if get_raw_value(hand) == (get_adjusted_value(hand) + (10 * hand.count('Ace'))):
        return False
    return True


def get_adjusted_value(hand):
    value = get_raw_value(hand)
    if 'Ace' not in hand:
        return value
    for _ in range(hand.count('Ace')):
        if value < 22:
            return value
        value -= 10
    return value


def get_raw_value(hand):
    value = 0
    for card in hand:
        value += CARDS[card]
    return value


def play_dealer(hand, shoe):
    while get_adjusted_value(hand) < 18:
        if get_adjusted_value(hand) == 17 and not is_soft(hand):
            break
        else:
            hand.append(shoe.hit())


def check_winner(player_hand, dealer_hand):
    player_val = get_adjusted_value(player_hand)
    dealer_val = get_adjusted_value(dealer_hand)
    if player_val > 21:
        return 'dealer'
    if dealer_val > 21:
        return 'player'
    if player_val > dealer_val:
        return 'player'
    if dealer_val > player_val:
        return 'dealer'
    return 'push'
