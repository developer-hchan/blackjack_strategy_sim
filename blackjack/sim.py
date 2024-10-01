import classes as cls
import functions as fun
import copy
import random

def simChoice(game: cls.Game, choice: str):
    for player in game.playerlist:
        for hand in player.player_hands:
            
            while True:
                fun.print_dealer_hand_hidden(game.dealer_hand)
                fun.print_hand(hand.hand, 'player')

                hand.hand_input = choice


                # Player schooses to stand
                if hand.hand_input == "stand":
                    break

                # Player chooses to hit
                elif hand.hand_input == "hit":
                    cls.draw(game.deck, hand.hand)
                    break


                #TODO: make this option toggable, based on if the game allows this function
                #Player chooses to surrender
                elif hand.hand_input == "surrender":
                    player.player_log.append(-hand.hand_bet*0.5)
                    player.player_wallet -= hand.hand_bet*0.5
                    hand.active = False
                    fun.print_hand(game.dealer_hand, 'dealer')
                    fun.print_hand(hand.hand, 'player')
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
                        cls.draw(game.deck, hand.hand)
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
                        cls.draw(hand.hand, player.player_hands[len(player.player_hands) - 2].hand)
                        # take another card from the deck and put it in the newly formed hand
                        cls.draw(game.deck, player.player_hands[len(player.player_hands) - 2].hand)

                        # takes the first card from current hand, adds it to the LAST hand in player_hands
                        cls.draw(hand.hand, player.player_hands[len(player.player_hands) - 1].hand)
                        # take another card from the deck and put it in the newly formed hand
                        cls.draw(game.deck, player.player_hands[len(player.player_hands) - 1].hand)
                        

                        # deactivating the current hand so it will not be evaluated, which should now be empty
                        hand.active = False

                        # back to the for loop to let the other hands be evaluated... well in theory
                        break
                
                # repeats the while loop, because a bad input was made
                else:
                    print('\n*****************************\n*bad input, please try again*\n*****************************\n')
                    continue



def simMatch(game: cls.Game, choice: str, baseDeck: list[cls.Card], dealer_faceUp: cls.Card):
    # TODO: make this editable, more easily, functionize

    # setting and resetting the game deck after every sim
    game.deck = copy.deepcopy(baseDeck)

    # setting player initial hand
    game.playerlist[0].player_hands[0].hand.append(cls.Card(10,'Heart'))
    game.playerlist[0].player_hands[0].hand.append(cls.Card(10,'Club'))

    # setting dealer's face up card
    game.dealer_hand.append(dealer_faceUp)

    # kill random amount of cards in a deck with at 0.25 worth of cards left -- assuming thats when the casino replaces the shoe
    # this is to simulate a random amount of matches being played before any given simulated match
    random.shuffle(game.deck)
    # choosing a random number of cards to kill
    kill = random.randint(0,round(0.75*len(game.deck)))
    for _ in range(kill):
        game.deck.pop(0)

    # dealer draws random face-down card from deck
    cls.draw(game.deck, game.dealer_hand)


    ### Now run a singular match of blackjack

    # checking wallet to make sure player has enought money to play
    fun.checkPlayerWallet(game)

    # placing bets on the hand, in this case the minimum
    fun.playerBetHands(game, game.minimum_bet)

    # checking to see if anyone got blackjack, to end match early I suppose
    fun.check4Blackjack(game)

    # simchoice and evaluation if the sim does not end early
    # NOTE: the line below only works with one player at the moment
    if any(hand.active == True for hand in game.playerlist[0].player_hands):
        
        # simulation choice
        simChoice(game, choice)

        # checking if player bust
        for player in game.playerlist:
            for hand in player.player_hands:

                # If hand busted (over 21)
                if hand.total > 21 and hand.active == True:
                    player.player_log.append(-hand.hand_bet)
                    player.player_wallet += -hand.hand_bet
                    hand.active = False
                    # fun.print_hand(game.dealer_hand, 'dealer')
                    # fun.print_hand(hand.hand, 'player')
                    # print('lose')
        
            
        # Dealer turn ~ dealer keeps hit until higher than 17. Equivalent to dealer doesn't hit soft 17
        while game.dealer_hand_total < 17:
            cls.draw(game.deck, game.dealer_hand)
        

        # final evaluation after game is done
        fun.evaluation(game)

        fun.clearGameHands(game)

    else:
        fun.clearGameHands(game)


##############################################################################################

def sim(dealer_faceUp: cls.Card, wallet = 100000, numberOfDecks = 6, choice = 'hit', numberOfMatches = 1000) -> list[float]:

    game = cls.Game()

    # making sure all player's have the minimum amount of money to play the match
    for idx, player in enumerate(game.playerlist):
        
        while True:
            try:
                # converting input to a float and rounding to 2 decimal places
                player.player_wallet = round(float(wallet), 2)
                print(f'\nConfirmed. Player has ${player.player_wallet}')
                break
            # If the user doesn't input a float or an int for their wallet, the program will fail to convert it to a float... i.e. float() and throw an error
            except:
                print('\nError occured, you did not input a valid number')
                continue

    # this is how we create shoes of decks
    copyDeck = copy.deepcopy(game.deck)
    baseCopyDeck = copy.deepcopy(game.deck)
    for _ in range(numberOfDecks - 1):
        baseCopyDeck.extend(copyDeck)


    # how many matches we want
    for _ in range(numberOfMatches):
        simMatch(game, choice, baseCopyDeck, dealer_faceUp)


    # print('PLAYER LOG START')
    # for x in game.playerlist[0].player_log:
    #     print(x)

    import statistics
    avgEV = statistics.fmean(game.playerlist[0].player_log)

    print(f'Player Avg EV for {choice}: {avgEV}')

    return avgEV


#############################################################################
data: list[tuple] = []

dealerSimCardList = [
    cls.Card(1,'heart'),
    cls.Card(2,'heart'),                
    cls.Card(3,'heart'),
    cls.Card(4,'heart'),
    cls.Card(5,'heart'),
    cls.Card(6,'heart'),
    cls.Card(7,'heart'),
    cls.Card(8,'heart'),
    cls.Card(9,'heart'),
    cls.Card(10,'heart')                 
                     ]

choice_list = ['hit','stand','surrender','double']

for dealer_card in dealerSimCardList:
    for player_choice in choice_list:
        avgEV = sim(dealer_faceUp=dealer_card, choice=player_choice, numberOfMatches=1000)

        # just need to put player hard total in here via the add()
        data.append((dealer_card.number, player_choice, avgEV))

for row in data:
    print(row)














