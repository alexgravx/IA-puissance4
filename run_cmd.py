# Pour jouer en ligne de commande

import argparse

from game import Game
from player import HumanPlayer, RandomPlayer
from ai_player import AIPlayer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', default='player 1')
    parser.add_argument('--p2', default='player 2')
    parser.add_argument('--rows', default='6', type=int)
    parser.add_argument('--cols', default='7', type=int)
    parser.add_argument('--num', default='4', type=int)
    args = parser.parse_args()

    player1 = HumanPlayer()
    player1.name=args.p1
    player2 = AIPlayer()
    player2.name=args.p2
    game = Game(player1, player2, args.cols, args.rows, args.num, verbose=True)
    game.run()
