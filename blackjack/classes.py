

# this is where the magic happens
class Game:
    def __init__(self):
        from classes import create_deck

        # by default, the game object will use a standard 52 deck
        self.deck: list[Card] = create_deck()

        # the dealer_hand playing the game
        self.dealer_hand: list[Card] = []

        # a game always needs at least one player
        player1 = Player()
        self.playerlist: list[Player] = [player1]

        # TODO: implement
        # Game variable that decides if the dealer hits or stands on a soft 17
        self.dealer_hit_on_soft_17 = False

        # TODO: implement game settings function somewhere
        # Game variable that decides what the minimum bet is
        # default minimum bet is $25.00
        self.minimum_bet: float = 25.00

        # TODO: add a dicitionary here as a game log
        # Dictionary of the results of every match

        # Usually when player hits a blackjack they are paid a bonus, varies game to game, but is usually a x1.5 bonus to the bet
        self.blackjack_bonus: float = 1.5
    
    # autoupdates the current total (int) in the dealer's hand
    @property
    def dealer_hand_total(self) -> int:
        return add(self.dealer_hand)

    #TODO: function allows the user to change default game settings before running a match
    def adjust_settings(self):

        pass
 
  
# Cards are objects
class Card:
    def __init__(self, number: int, suit: str):
        self.number = number
        self.suit = suit
        self.soft = False

        # an Ace can be 'soft', which means it's value can be 1 or 11; whichever is more beneficial
        # this line makes all ace's soft by default... this is helpful when adding up hand totals
        if self.number == 1:
            self.soft = True


    def __str__(self):
        # This line is to make aces more clear to the player when playing game (which value the ace currently is)
        if self.number == 1 or self.number == 11:
            return f"Ace of {self.suit}s"
        else:
            return f"{self.number} of {self.suit}s"


# adds together the values of the cards in the inputted hand (dealer or player)
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


# A hand of Cards that goes to a player
class Hand:
        
    def __init__(self, bet=0.00):
        self.hand: list[Card] = []

        # how much the player is currently betting
        self.hand_bet: float = bet

        # this is used to see if a hand has already been evaluated
        self.active = True

        # the player's choice on what to do dfor each hand
        self.hand_input: str = None

    # get current int total of hand; auto-updates
    @property
    def total(self) -> int:
        return add(self.hand)


# a Player can have multiple Hands
class Player:

    def __init__(self):

        # all the hands the player has, starting with an initial hand by default
        hand = Hand()
        self.player_hands: list[Hand] = [hand]

        # how much money the player has
        self.player_wallet: float = 0.00

        # records the plus/minus of the player's choices
        self.player_log: list[float] = []


    # the total bet from all the player's hands
    @property
    def player_betStack(self) -> float:
        
        betStack = 0

        for hand in self.player_hands:
            betStack += hand.hand_bet

        return betStack


    # adding a Hand Object to a Player Object
    def add_hand(self, bet):
        self.player_hands.append(Hand(bet))


# adds a card from the game.deck into the inputted hand (dealer or player)
def draw(deck: list[Card], hand: list[Card]) -> None:
    import random

    # generates a random idx
    idx = random.randint(0,len(deck)-1)

    hand.append(deck[idx])
    deck.pop(idx)
    

# adds a card from the game.deck into the inputted hand (dealer or player)
def draw_notRandom(deck: list[Card], hand: list[Card], idx: int) -> None:

    hand.append(deck[idx])
    deck.pop(idx)



