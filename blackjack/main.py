# Have a game object
from classes import *
from functions import match
game = Game()

# a function to adjust default game settings, eles use init default
#game.adjust_settings()

# initial wallet of all players in the game
for idx, player in enumerate(game.playerlist):
     
    while True:
        try:
            # converting input to a float and rounding to 2 decimal places
            player.player_wallet = round(float(input('how much money is in your wallet?: ')) , 2)
            print(f'\nConfirmed. Player has ${player.player_wallet}')
            break
        # If the user doesn't input a float or an int for their wallet, the program will fail to convert it to a float... i.e. float() and throw an error
        except:
            print('\nError occured, you did not input a valid number')
            continue
    

# shuffling deck
shuffleDeck(game.deck)

# a single match of a blackjack game -> return plus/minus
match(game)
match(game)

print('\n')

# NOTE: temporary, just to makes sure that I'm getting the expected outputs
for player in game.playerlist:
    
    for x in player.player_log:
        print(f'player log: {x}')
    
    print(f'player wallet: {player.player_wallet}')


