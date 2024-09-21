from classes import *
from functions import *

def main():

    game = Game()

    # This loop sets the player's wallet
    # Player Wallet is a Game Variable, set when a Game is created. That way it can be updated and acted upon in between multiple matches being run
    while True:
        try:
            # converting input to a float and rounding to 2 decimal places
            game.player_wallet = round(float(input('how much money is in your wallet?: ')) , 2)
            print(f'\nConfirmed. Player has ${game.player_wallet}')
            break
        # If the user doesn't input a float or an int for their wallet, the program will fail to convert it to a float... i.e. float() and throw an error
        except:
            print('Error occured, you did not input a valid number\n')
            continue
    
    # for _ in range(1):
    #     temp = game.match()
    #     print(temp)
    #     update_wallet(game,temp)
    #     print(game.player_wallet)

    temp = game.match()
    print(temp)



# function that updates game.player_wallet after 
def update_wallet(game: Game, temp: tuple[str,float]): # tuple is size 2
    try:
        game.player_wallet += temp[1]
    except:
        print('Unexpected error when updating wallet')


    

    




if __name__ == "__main__":
    main()