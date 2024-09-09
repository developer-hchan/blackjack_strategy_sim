

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


    # Game variable that decides if the dealer hits or stands on a soft 17
    dealer_hit_on_soft_17 = False


    
    # runs one round of a blackjack game (makes it easy to simulate by running as many rounds as we want)
    def round(self) -> str: # function can return 'win','lose','tie'
        from functions import draw
        from functions import add

        # dealer and player get their starting hands
        draw(self.deck, self.player_hand)
        draw(self.deck, self.dealer_hand)
        draw(self.deck, self.player_hand)
        draw(self.deck, self.dealer_hand)


        self.dealer_hand_total = add(self.dealer_hand)
        self.player_hand_total = add(self.player_hand)


        # Check if dealer has 21 (blackjack)
        if self.dealer_hand_total == 21:
            # if player also has 21, then the round ends in a tie, a.k.a 'push'
            if self.player_hand_total == 21:
                # this just shows dealer's and player's hands
                print_hands(self)
                print('tie')
                # need a return value for when simulations are run to tally
                return 'tie'
            else:
                print_hands(self)
                print('lose')
                return 'lose'
            
        
        # Check if player has 21 (blackjack), if so, is immediately paid out... already checked if dealer has 21 above
        if self.player_hand_total == 21:
            print_hands(self)
            print('win')
            return 'win'



        ## This is where player input starts
        #if no one wins, they start player input (player turn) probably needs to be in while True loop
        # all break statements just serve to end the player's turn, i.e. the while True loop
        while True:
            print_hands_hidden(self)
            self.player_input = input("what would you like to do?: \n")

            if self.player_input == "stand":
                break

            elif self.player_input == "hit":
                draw(self.deck, self.player_hand)
                self.player_hand_total = add(self.player_hand)

                if self.player_hand_total == 21:
                    break
                elif self.player_hand_total > 21:
                    break
                else:
                    continue

            
            #TODO: implement when betting is a part of the game
            elif self.player_input == "split":
                pass

            #TODO: implement when betting is a part of the game
            elif self.player_input == "double":
                pass

            else:
                print('\n*****************************\n*bad input, please try again*\n*****************************\n')
                continue


        # If player busted (over 21)
        if self.player_hand_total > 21:
            print_hands(self)
            print('lose')
            return 'lose'

        #TODO: add a check if the rules state a dealer hits on a soft 17
        # Dealer turn ~ dealer keeps hit until higher than 17
        while self.dealer_hand_total < 17:
            draw(self.deck, self.dealer_hand)
            self.dealer_hand_total = add(self.dealer_hand)


        ### checking the results of both turns, assuming the player's turn didn't terminate early

        # if dealer bust, palyer immediate win
        if self.dealer_hand_total > 21:
            print_hands(self)
            print('win')
            return 'win'
        
        # if dealer and player have the same total
        if self.dealer_hand_total == self.player_hand_total:
            print_hands(self)
            print('tie')
            return 'tie'
        # if dealer has higher
        if self.dealer_hand_total > self.player_hand_total:
            print_hands(self)
            print('lose')
            return 'lose'
        
        # if player has higher
        if self.player_hand_total > self.dealer_hand_total:
            print_hands(self)
            print('win')
            return 'win'
        

 
        
        # if we ever get to this piece of code, something went wrong lol
        print('unexpected program end')




# The purpose of this function is so that I can write less print statements in the round() function
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
    print('** DEALER HIDDEN CARD **')
    print(f'dealer has a {game.dealer_hand[0]} face up\n')

    for card in game.player_hand:
        print(card)
    print(f"player has: {game.player_hand_total}\n")


    













    





