from time import sleep
from main import Game

p1_name = 'Alex'
p2_name = 'Max'
game = Game(p1_name, p2_name)

# for _ in range(1000):
#     game = Game(p1_name, p2_name)
#     print(game.starts(game.player1_hand, game.player2_hand, game.trump_card))
counter = 0


def test():
    while True:
        print(f'{" " * 12}{"-" * 17}\n{" " * 13}Welcome to MiMa\n{" " * 12}{"-" * 17}\n')
        start_input = input('Do you want to play Durak-Game? [Y]es/[N]o: ')
        if start_input.lower() == 'yes' or start_input.lower() == 'y':
            print('Game starts...\n\n')
            sleep(1.1)
            deck_of_cards = game.deck
            p1_hand = game.player1_hand
            p2_hand = game.player2_hand
            trump_c = game.trump_card
            cards_on_table = []
            print('player1 cards: ', p1_hand, '\nplayer2 cards: ', p2_hand, '\n')
            print('Trump card: ', trump_c, '\n')
            print(game.starts(p1_hand, p2_hand, trump_c), 'starts the game!')
        else:
            print('\nExit 0')
            break


