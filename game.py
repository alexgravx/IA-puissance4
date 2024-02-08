import random

import utils
from board import Board


class Game(object):
    """Generic class to run a game."""
    def __init__(
            self, player1, player2, cols=7, rows=6, winning_length=4,
            verbose=False):
        self.winning_length = winning_length
        self.board = Board(num_rows=rows, num_cols=cols)
        self.players = [player1, player2]
        self.verbose = verbose
        self.reset()

    def getWinner(self, pos):
        """Returns the player (boolean) who won, or None if nobody won"""
        tests = []
        tests.append(self.board.getCol(pos[0]))
        tests.append(self.board.getRow(pos[1]))
        tests.append(self.board.getDiagonal(True, pos[0] - pos[1]))
        tests.append(self.board.getDiagonal(False, pos[0] + pos[1]))
        for test in tests:
            color, size = utils.longest(test)
            if size >= self.winning_length:
                for player in self.players:
                    if player.color == color:
                        return player

    def isOver(self):
        return self.winner is not None or self.board.isFull()

    def reset(self, randomStart=False):
        self.board.reset()
        self.winner = None
        # Make sure one player is 1 the other -1
        self.players[0].color = 1
        self.players[1].color = -1
        self.currPlayer = int(random.random() > 0.5) if randomStart else 0

    def mayShowDebug(self):
        if not self.verbose:
            return

        print(self.board, '\n')
        if not self.isOver():
            return

        if self.winner is not None:
            print("{0} ({1}) wins!".format(
                self.winner.name, Board.valueToStr(self.winner.color)))
        else:
            print("It's a draw!")

    def run(self, randomStart=False):
        """This method runs the game, alterating between the players."""
        self.reset(randomStart)
        while not self.isOver():
            # TODO(student): !!! use the `observe` method of the Player to learn
            # the moves as the game goes !!!
            player = self.players[self.currPlayer]

            col = player.getColumn(self.board)
            row = self.board.play(player.color, col)
            pos = (col, row)
            if pos not in self.board:
                continue

            self.mayShowDebug()
            print("winner",self.getWinner(pos))
            self.winner = self.getWinner(pos)
            self.currPlayer = (self.currPlayer + 1) % 2

        self.mayShowDebug()

    def train(self, num_episodes):
        scores = [0, 0]
        for k in range(num_episodes):
            self.run(randomStart=True)
            if self.winner:
                for idx, player in enumerate(self.players):
                    if player.color == self.winner.color:
                        scores[idx] += 1
                        break

            if k % 10 == 0:
                print('episode {0}: {1}'.format(k, scores))
