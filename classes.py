

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
        # This is to make aces more clear to the player when playing game
        if self.number == 1 or self.number == 11:
            return f"Ace of {self.suit}s"
        else:
            return f"{self.number} of {self.suit}s"


# NOTE: have to import create_deck() after the concept of a Card object is created because create_deck() relies on card objects existing;



class Game:
    

    def __init__(self):
        from functions import create_deck

        self.deck: list[Card] = create_deck()

        self.dealer_hand: list[Card] = []
        self.player_hand: list[Card] = []

        self.dealer_hand_total: int = 0
        self.player_hand_total: int = 0

        # the player's choice on what to do during their turn
        self.player_input: str = None

        # the player's wallet
        self.player_wallet: int = 0

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


    
    # runs one match of a blackjack game (makes it easy to simulate by running as many matches as we want)
    def match(self) -> tuple[str,float]: # str is 'win','lose','tie'; float is the plus/minus (how much the user won / lost in the match)
        from functions import draw
        from functions import add

        double_bet = 1

        # if player wallet is less than minimum bet
        if self.player_wallet < self.minimum_bet:
            print(f'Player has ${self.player_wallet}, ${self.minimum_bet} is needed to play a match')
            return
        #NOTE: check if this else statement causes problems in the future... right now, it is not interferring with the if statements below...
        else:
            print(f'Player\'s current wallet: {self.player_wallet}')


        # the first thing that happens in a match is that the player must bet money
        while True:
            try:
            # round(float(... , 2)) used to convert user input into a float and then round to 2 decimal places
                player_bet = round(float(input(f'\nhow much would you like to bet? For this game, bet minimum is ${self.minimum_bet}: ')) , 2)

                if player_bet >= self.minimum_bet:
                    print(f'\nConfirmed. Player has bet ${player_bet} on this match')
                    break
                else:
                    print(f'Error occured, your bet of ${player_bet} is less than the minimum bet of ${self.minimum_bet}\n')
                    continue

            # if the code in the try block fails to convert the input into a float, the exception block will run
            except:
                print('Error occured, you did not input a valid number for your bet\n')
                continue
        
        

        # dealer and player get their starting hands and starting hand totals
        draw(self.deck, self.player_hand)
        draw(self.deck, self.dealer_hand)
        draw(self.deck, self.player_hand)
        draw(self.deck, self.dealer_hand)


        self.dealer_hand_total = add(self.dealer_hand)
        self.player_hand_total = add(self.player_hand)


        # Check if dealer has 21 (blackjack)
        if self.dealer_hand_total == 21:
            # if player also has 21, then the match ends in a tie, a.k.a 'push'
            if self.player_hand_total == 21:
                # this just shows dealer's and player's hands
                print_hands(self)
                print('tie')
                # need a return value for when simulations are run to tally
                teardown_hands(self.dealer_hand, self.player_hand)
                return ('tie',0)
            else:
                print_hands(self)
                print('lose')
                teardown_hands(self.dealer_hand, self.player_hand)
                return ('lose',-player_bet)
            
        
        # Check if player has 21 (blackjack), if so, is immediately paid out... already checked if dealer has 21 above
        if self.player_hand_total == 21:
            print_hands(self)
            print('win')
            teardown_hands(self.dealer_hand, self.player_hand)
            return ('win',player_bet*self.blackjack_bonus) # adjustable in game variables


        



        ## This is where player input starts
        #if no one wins, they start player input (player turn) probably needs to be in while True loop
        # all break statements just serve to end the player's turn, i.e. the while True loop
        while True:
            print_hands_hidden(self)
            self.player_input = input("what would you like to do?: \n")

            # Player schooses to stand
            if self.player_input == "stand":
                break

            # Player chooses to hit
            elif self.player_input == "hit":
                draw(self.deck, self.player_hand)
                self.player_hand_total = add(self.player_hand)

                if self.player_hand_total == 21:
                    break
                elif self.player_hand_total > 21:
                    break
                else:
                    continue

            # Player chooses to surrender
            #TODO: make this option toggable, based on if the game allows this function


            # Player chooses to "double down" a.k.a "double"
            # Doubling means doubling your bet in exchange for only drawing one card
            # TODO: add a check to make sure the player has enough money to even double down
            elif self.player_input == "double":
                draw(self.deck, self.player_hand)
                self.player_hand_total = add(self.player_hand)
                # double bet is multiplied to every bet before this function returns the bet value
                double_bet = 2
                break


            #TODO: implement when betting is a part of the game
            elif self.player_input == "split":
                pass

            

            else:
                print('\n*****************************\n*bad input, please try again*\n*****************************\n')
                continue


        # If player busted (over 21)
        if self.player_hand_total > 21:
            print_hands(self)
            print('lose')
            teardown_hands(self.dealer_hand, self.player_hand)
            return ('lose',-player_bet*double_bet) #if the player doubled, double_bet is 2, else it is 1, player bet is negative because player lost

        #TODO: add a check if the rules state a dealer hits on a soft 17
        # Dealer turn ~ dealer keeps hit until higher than 17
        while self.dealer_hand_total < 17:
            draw(self.deck, self.dealer_hand)
            self.dealer_hand_total = add(self.dealer_hand)


        ### checking the results of both turns, assuming the player's turn didn't terminate early

        # if dealer bust, player immediate win
        if self.dealer_hand_total > 21:
            print_hands(self)
            print('win')
            teardown_hands(self.dealer_hand, self.player_hand)
            return ('win',player_bet*double_bet)
        
        # if dealer and player have the same total
        if self.dealer_hand_total == self.player_hand_total:
            print_hands(self)
            print('tie')
            teardown_hands(self.dealer_hand, self.player_hand)
            return ('tie',0)
        
        # if dealer has higher
        if self.dealer_hand_total > self.player_hand_total:
            print_hands(self)
            print('lose')
            teardown_hands(self.dealer_hand, self.player_hand)
            return ('lose',-player_bet*double_bet)
        
        # if player has higher
        if self.player_hand_total > self.dealer_hand_total:
            print_hands(self)
            print('win')
            teardown_hands(self.dealer_hand, self.player_hand)
            return ('win',player_bet*double_bet)
        

 
        
        # if we ever get to this piece of code, something went wrong lol
        print('unexpected program end')




# The purpose of this function is so that I can write less print statements in the match() function
def print_hands(game: Game):
    print("\n")

    for card in game.dealer_hand:
        print(card)
    print(f"dealer has: {game.dealer_hand_total}\n")

    for card in game.player_hand:
        print(card)
    print(f"player has: {game.player_hand_total}\n")


# this is the print hands function that hides one of the dealer's cards from the player
def print_hands_hidden(game: Game):
    print("\n")
    
    print(game.dealer_hand[0])
    print('? of ?')
    print(f'dealer has: {game.dealer_hand[0]} + ?\n')

    for card in game.player_hand:
        print(card)
    print(f"player has: {game.player_hand_total}\n")


#
def setup_hands():
    pass

# will probably adjust after the split method is defined, because the split method is the only way more than two hands are present
def teardown_hands(*hands: list[object]):
    for hand in hands:
        hand.clear()
    


    













    





