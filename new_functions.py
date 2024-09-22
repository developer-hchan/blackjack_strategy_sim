from new_classes import Game

# 1 round / match of blackjack
# maybe a generator that stores results, then 
def match(game: Game) -> None: # Just updates player.player_log and player.player_wallet

    from functions import draw


    # Checking all player's wallets, making sure they can bet the minimum at least before the match starts
    # NOTE: may need to add some functionality to add players to game somewhere
    for idx, player in enumerate(game.playerlist):

        if player.player_wallet < game.minimum_bet:
            print(f'Player has ${player.player_wallet}, ${game.minimum_bet} is needed to play a match')
            game.playerlist.pop(idx)

            # in case there was only one player in the game, and they were removed, need to end the match because it can't be played
            if len(game.playerlist) == 0:
                print('game lacks players to be played')
                return
            else:
                continue

        #NOTE: check if this else statement causes problems in the future... right now, it is not interferring with the if statements below...
        else:
            print(f'Player\'s current wallet: {player.player_wallet}')


    # deal starting cards (2 cards) to everyone, including the dealer, going around in a circle
    for _ in range(2):

        # each players' hand(s) draws a card
        for player in game.playerlist:
            for hand in player.player_hands:
                # NOTE: hand.hand ... hand. is the hand object ... .hand is the list of cards in the hand object
                draw(game.deck, hand.hand)

        # dealer draws
        draw(game.deck, game.dealer_hand)
    

    ### NOTE: need to change things starting from here to hand.hand, which is the actual list of cards in the hand object

    # the first thing that happens in a match is that the player(s) must bet money for each of their hands
    for player in game.playerlist:
        for hand in player.player_hands:

            while True:
                try: # ... round(float(... , 2)) converts user input into a float and then rounds to 2 decimal places
                    hand.hand_bet = round(float(input(f'\nhow much would you like to bet? For this game, bet minimum is ${game.minimum_bet}: ')) , 2)

                    if hand.hand_bet >= game.minimum_bet:
                        print(f'\nConfirmed. Player has bet ${hand.hand_bet} on this match')
                        break
                    else:
                        print(f'Error occured, your bet of ${hand.hand_bet} is less than the minimum bet of ${game.minimum_bet}\n')
                        continue

                # if the code in the try block fails to convert the input into a float, the exception block will run
                except:
                    print('Error occured, you did not input a valid number for your bet\n')
                    continue


    ###
    ### Starting Evaluations of all hands and all players
    ###
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
            

            ## Player options for every hand now, if no automatic wins
            while True:
                print_dealer_hand_hidden(game.dealer_hand)
                print_hand(hand.hand, 'player')
                hand.hand_input = input("what would you like to do?: \n")

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

                # Player chooses to surrender
                #TODO: make this option toggable, based on if the game allows this function


                # Player chooses to "double down" a.k.a "double"
                # Doubling means doubling your bet in exchange for only drawing one card
                # TODO: add a check to make sure the player has enough money to even double down
                elif hand.hand_input == "double":
                    pass

                #TODO: implement when betting is a part of the game
                elif hand.hand_input == "split":
                    pass


                else:
                    print('\n*****************************\n*bad input, please try again*\n*****************************\n')
                    continue

            ## final evaluation w/o dealer
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


    ###
    ### Final Evaluation After Player and Dealer have gone
    ###

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
            if hand.total > game.dealer_hand_total:
                player.player_log.append(hand.hand_bet)
                player.player_wallet += hand.hand_bet
                hand.active = False
                print_hand(game.dealer_hand, 'dealer')
                print_hand(hand.hand, 'player')
                print('win')

    return            






# The purpose of this function is so that I can write less print statements in the match() function
def print_hand(hand, person: str): # person can be 'dealer' or 'player'
    from new_classes import add

    print("\n")

    for card in hand:
        print(card)
    print(f"{person} has: {add(hand)}\n")


# this is the print hands function that hides one of the dealer's cards from the player
def print_dealer_hand_hidden(dealer_hand):
    print("\n")
    
    # dealer face down card
    print('? of ?')

    # dealer face up card
    print(dealer_hand[0])

    print(f'dealer has: {dealer_hand[0]} + ?\n')

