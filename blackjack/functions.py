from classes import Game


# The purpose of this function is so that I can write less print statements in the match() function
def print_hand(hand, person: str): # person can be 'dealer' or 'player'
    from classes import add

    # player hand total
    print(f"\n{person} has a hand total of: {add(hand)}")

    # player's cards
    for card in hand:
        print(f'card: {card}')


# this is the print hands function that hides one of the dealer's cards from the player
def print_dealer_hand_hidden(dealer_hand):
    
    #showing dealer face up card
    print(f'\ndealer has a {dealer_hand[0]} + ? for a total of: ?')

    # dealer face up card
    print(f'card: {dealer_hand[0]}')
    
    # dealer face down card
    print('card: ? of ?')


# Checking all player's wallets, making sure they can bet the minimum at least before the match starts
def checkPlayerWallet(game: Game):
    for idx, player in enumerate(game.playerlist):

        if player.player_wallet < game.minimum_bet:
            print(f'Player has ${player.player_wallet}, ${game.minimum_bet} is needed to play a match')
            # removing a player without enough money from the game
            game.playerlist.pop(idx)

            # in case there was only one player in the game, and they were removed, need to end the match because it can't be played
            if len(game.playerlist) == 0:
                # TODO: eventually give players a str function, and generate names
                print(f'player has been removed due to lack of funds')
                print('game lacks players to be played')
                return
            else:
                continue

        else:
            print(f'\nPlayer\'s current wallet: {player.player_wallet}')


# TODO: update python console response (print statements) to include the names of each hand
# TODO: probably update the Hand() class to include a name object that generators new names from a seperate integer generator
# TODO: and a __str__ method
# player's bet money on all their hand for the match
def playerBetHands(game: Game, sim_bet: float = None):

    for player in game.playerlist:
        for hand in player.player_hands:
            
            if sim_bet == None:
                while True:
                    try: # ... round(float(... , 2)) converts user input into a float and then rounds to 2 decimal places
                        hand.hand_bet = round(float(input(f'\nhow much would you like to bet? For this game, bet minimum is ${game.minimum_bet}: ')) , 2)

                        if hand.hand_bet >= game.minimum_bet:
                            print(f'\nConfirmed. Player has bet ${hand.hand_bet} on this match')
                            break
                        else:
                            print(f'\nError occured, your bet of ${hand.hand_bet} is less than the minimum bet of ${game.minimum_bet}')
                            continue

                    # if the code in the try block fails to convert the input into a float, the exception block will run
                    except:
                        print('\nError occured, you did not input a valid number for your bet')
                        continue
            else:
                hand.hand_bet = sim_bet


# Card evaluation I: Checking for blackjacks from the dealer and players in the game
def check4Blackjack(game: Game) -> None: # just updates player_log and hand.active if applicable
    for player in game.playerlist:
        for hand in player.player_hands:

            # Check if dealer automatically wins by having 21 (blackjack)
            if game.dealer_hand_total == 21:

                # if player also has 21, then the match ends in a tie, a.k.a 'push'
                if hand.total == 21:
                    # appends a plus/minus of 0 to log
                    player.player_log.append(0.00)

                    #hand.active just checks if the hand has already been evaluated, so it won't be evaluated again later
                    hand.active = False

                    print_hand(game.dealer_hand, 'dealer')
                    print_hand(hand.hand, 'player')
                    print('tie')
                
                else:
                    player.player_log.append(-hand.hand_bet)

                    # player wallet lose money based on amoung bet on the hand
                    player.player_wallet += -hand.hand_bet
                    hand.active = False
                    print_hand(game.dealer_hand, 'dealer')
                    print_hand(hand.hand, 'player')
                    print('lose')
            
            ## If dealer didn't automatically win, then time to evaluate the player's cards
            # Check if player has 21 (blackjack), if so, is immediately paid out... already checked if dealer has 21 above
            if hand.total == 21 and hand.active == True:
                player.player_log.append(hand.hand_bet)
                player.player_wallet += hand.hand_bet
                hand.active = False
                
                print_hand(game.dealer_hand, 'dealer')
                print_hand(hand.hand, 'player')
                print('win')

##NOTE: eventually there will be an issue with mutliple hands, of certain options, like automatic blackjacks or surrenders showing the dealer's hand (to include the face down card)
##NOTE: before potentially all hands are played; however, it works with only one player in the game for now
## player choice on what to do with their hands
def playerChoice(game: Game, choice: str = None):

    from classes import draw
    
    #TODO: add the hand's name to console printout when making choices, and I suppose also give hands a name attribute

    for player in game.playerlist:
        for hand in player.player_hands:
            
            # If current hand still needs to be evaluated / worked on
            if hand.active == True:
                while True:
                    print_dealer_hand_hidden(game.dealer_hand)
                    print_hand(hand.hand, 'player')

                    #NOTE: this check below is for testing purpose, and won't work with multiple hands, so it's temporary
                    # for multiple hands probably need to make the while and for loop external, and make some return so the external while can work
                    if choice != None:
                        hand.hand_input = choice
                    else:
                        hand.hand_input = input("\nwhat would you like to do?: \n")


                    # Player schooses to stand
                    if hand.hand_input == "stand":
                        break

                    # Player chooses to hit
                    elif hand.hand_input == "hit":
                        draw(game.deck, hand.hand)

                        if hand.total == 21:
                            break
                        elif hand.total > 21:
                            break
                        else:
                            continue

                    #TODO: make this option toggable, based on if the game allows this function
                    #Player chooses to surrender
                    elif hand.hand_input == "surrender":
                        player.player_log.append(-hand.hand_bet*0.5)
                        player.player_wallet -= hand.hand_bet*0.5
                        hand.active = False
                        print_hand(game.dealer_hand, 'dealer')
                        print_hand(hand.hand, 'player')
                        print('lose, half bet taken')
                        break


                    # Player chooses to "double down" a.k.a "double": This means doubling your bet in exchange for only drawing one card
                    elif hand.hand_input == "double":
                        
                        # player.player_betStack + hand.hand_bet === putting hand.hand_bet*2 in the betStack effectively
                        if player.player_betStack + hand.hand_bet > player.player_wallet:
                            print(f'\nPlayer wallet has ${player.player_wallet}, which is not enough to double down')
                            continue
                        elif len(hand.hand) != 2:
                            print(f'\nPlayer cannot double as they have already hit')
                            continue
                        else:
                            # doubling the bet on hand
                            hand.hand_bet *= 2
                            # double down is only allowed to draw one card
                            draw(game.deck, hand.hand)
                            break


                    # Player chooses to split
                    elif hand.hand_input == "split":

                        # splitting effectively doubles your bet, since the same size bet needs to be put on the new hand
                        # player.player_betStack + hand.hand_bet === putting hand.hand_bet*2 in the betStack effectively
                        if player.player_betStack + hand.hand_bet > player.player_wallet:
                            print(f'\nPlayer wallet has ${player.player_wallet}, which is not enough to split')
                            continue
                        elif len(hand.hand) != 2:
                            print(f'\nPlayer cannot split as they do not have 2 cards in their hand')
                            continue
                        elif hand.hand[0].number != hand.hand[1].number:
                            print(f'\nPlayer cannot split as they do not have 2 matching cards')
                            continue
                        # creating two new hands and putting them in player.player_hands; deactivating current hand so it won't be evaluated
                        else:
                            # creates and appends two new hands with bets equivalent to the orginal hand
                            player.add_hand(hand.hand_bet)
                            player.add_hand(hand.hand_bet)
                            

                            # takes the first card from current hand, adds it to the 2ND TO LAST hand in player_hands
                            draw(hand.hand, player.player_hands[len(player.player_hands) - 2].hand)
                            # take another card from the deck and put it in the newly formed hand
                            draw(game.deck, player.player_hands[len(player.player_hands) - 2].hand)

                            # takes the first card from current hand, adds it to the LAST hand in player_hands
                            draw(hand.hand, player.player_hands[len(player.player_hands) - 1].hand)
                            # take another card from the deck and put it in the newly formed hand
                            draw(game.deck, player.player_hands[len(player.player_hands) - 1].hand)
                            

                            # deactivating the current hand so it will not be evaluated, which should now be empty
                            hand.active = False

                            # back to the for loop to let the other hands be evaluated... well in theory
                            # NOTE: may not work
                            break
                    
                    # repeats the while loop, because a bad input was made
                    else:
                        print('\n*****************************\n*bad input, please try again*\n*****************************\n')
                        continue
            
            # goes to this else if hand.active is false for current hand; continues the "for loop", not the "while loop"
            else:
                continue
        

def evaluation(game: Game) -> None:
    for player in game.playerlist:
        for hand in player.player_hands:

            # if dealer bust, player immediate win
            if game.dealer_hand_total > 21 and hand.active == True:
                player.player_log.append(hand.hand_bet)
                player.player_wallet += hand.hand_bet
                hand.active = False
                print_hand(game.dealer_hand, 'dealer')
                print_hand(hand.hand, 'player')
                print('win')
            
            # if dealer and player have the same total
            if game.dealer_hand_total == hand.total and hand.active == True:
                player.player_log.append(0.00)
                hand.active = False
                print_hand(game.dealer_hand, 'dealer')
                print_hand(hand.hand, 'player')
                print('tie')
            
            # if dealer has higher
            if game.dealer_hand_total > hand.total and hand.active == True:
                player.player_log.append(-hand.hand_bet)
                player.player_wallet += -hand.hand_bet
                hand.active = False
                print_hand(game.dealer_hand, 'dealer')
                print_hand(hand.hand, 'player')
                print('lose')
            
            # if player has higher
            if hand.total > game.dealer_hand_total and hand.active == True:
                player.player_log.append(hand.hand_bet)
                player.player_wallet += hand.hand_bet
                hand.active = False
                print_hand(game.dealer_hand, 'dealer')
                print_hand(hand.hand, 'player')
                print('win')


# 1 round / match of blackjack
def match(game: Game) -> None: # Just updates player.player_log and player.player_wallet
    from classes import draw

    # NOTE: may need to add some functionality to add players to game somewhere

    # Checking all player's wallets, making sure they can bet the minimum at least before the match starts
    checkPlayerWallet(game)

    # deal starting cards (2 cards) to everyone, including the dealer, going around in a circle
    for _ in range(2):
        # each players' hand(s) draws a card
        for player in game.playerlist:
            for hand in player.player_hands:
                # NOTE: hand.hand ... hand. is the hand object ... .hand is the list of cards in the hand object
                draw(game.deck, hand.hand)

        # dealer draws
        draw(game.deck, game.dealer_hand)
    
    # The first thing that happens in a match is that the player(s) must bet money for each of their hands
    playerBetHands(game)

    # checking to see if the dealer or the player automatically wins from blackjack
    check4Blackjack(game)
    
    # if there are still active hands in the game that need to be acted upon, continue, else, just end match() early
    if any(hand.active == True for hand in player.player_hands): 
        # player's choose what to do with all their hands
        playerChoice(game)

        ## checking if player's busted before the dealer draws (this is how they do it in the casinos)
        for player in game.playerlist:
            for hand in player.player_hands:

                # If hand busted (over 21)
                if hand.total > 21 and hand.active == True:
                    player.player_log.append(-hand.hand_bet)
                    player.player_wallet += -hand.hand_bet
                    hand.active = False
                    print_hand(game.dealer_hand, 'dealer')
                    print_hand(hand.hand, 'player')
                    print('lose')
    
        #TODO: add a check if the rules state a dealer hits on a soft 17
        # Dealer turn ~ dealer keeps hit until higher than 17
        while game.dealer_hand_total < 17:
            draw(game.deck, game.dealer_hand)

        ### Final Evaluation After Player and Dealer have fnished
        evaluation(game)

        # clearing all hands
        clearGameHands(game)
    
    else:
        clearGameHands(game)
        return


# clears the hand of the players in game
def clearGameHands(game: Game):
    from classes import Hand

    # reseting dealer's hand
    game.dealer_hand = []
    
    # all player's get reset to having one empty hand at the end of a match
    for player in game.playerlist:
        player.player_hands = [Hand()]




