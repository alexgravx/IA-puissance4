import argparse

from player import HumanPlayer, RandomPlayer
from ai_player import AIPlayer
from ui_game import UIGame


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', default='player 1')
    parser.add_argument('--p2', default='player 2')
    args = parser.parse_args()

    player1 = AIPlayer()
    player1.name=args.p1
    player2 = HumanPlayer()
    player2.name=args.p2

    game = UIGame(player1, player2)
