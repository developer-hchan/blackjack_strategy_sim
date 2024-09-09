from classes import Card
import random

# Creating a deck of cards
def create_deck() -> list[Card]:

    deck = []
    suits = ['Heart','Diamond','Spade','Club']

    # Creates 52 card objects; starts with the 4 suits H, D, S, C and gives each suit 13 numbers
    for x in suits:
        # range(1,14) has 13, which includes J,Q,K: 11 == J, 12 == Q, 13 == K
        for y in range(1,14):
            # Card(number, suit)
            # Card(number) is min(y,10) because 10, J, Q, and K all have a value of 10 in the game of blackjack
            deck.append(Card(min(y,10) , x))
    
    return deck



# adds a card from the game.deck into the inputted hand (dealer or player)
def draw(deck: list[Card], hand: list[Card]) -> None:
    # generates a random idx
    idx = random.randint(0,len(deck)-1)

    hand.append(deck[idx])
    deck.pop(idx)



# add together the values of the cards in the inputted hand (dealer or player)
def add(hand: list[Card]) -> int:
    
    # Job of the ace_in_hand is to keep track of how many aces are in the hand
    ace_in_hand = 0
    # counter keeps track of how many times the while loop runs
    counter = 0
    

    # Changing all aces in hand to a soft value of 11... Card.number = 11
    for card in hand:
        if card.soft == True:
            card.number = 11
            ace_in_hand += 1

    # counter keeps track of how many times the while loop runs... should only run extra times if we have aces in hand (ace_in_hand != 0) because making the ace hard could
    # lower the hand total
    while counter <= ace_in_hand:
        counter += 1
        total = 0

        # the first totaling
        for card in hand:
                total += card.number
    
        # in case we are over 21 and still have soft aces in the hand
        if total > 21:

            # changes only one ace from hard to soft
            for card in hand:
                if card.soft == True:
                    card.soft = False
                    card.number = 1
                    
                    # Should break the for loop, so in the case there are multiple aces in hand, only one ace is made hard and then the process repeats with the While loop
                    break
        
    
    return total

