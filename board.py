from utils import longest
from mesure_time import timeit

class Board(object):
    """This class represents the board of the connect4 games, with all the
    necessary operations to play a game"""
    def __init__(self, num_rows=6, num_cols=7):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.diagRanges = {
            True: range(-self.num_rows, self.num_cols),
            False: range(self.num_cols + self.num_rows)
        }
        self.reset()

    def reset(self):
        self.board = [[0] * self.num_rows for i in range(self.num_cols)]

    def __contains__(self, position):
        return 0 <= position[0] < self.num_cols and \
            0 <= position[1] < self.num_rows

    def __getitem__(self, position):
        if isinstance(position, tuple):
            if position in self:
                return self.board[position[0]][position[1]]
        else:
            return self.board[position]

    @staticmethod
    def valueToStr(value):
        toStr = {1: "x", -1: 'o'}
        return toStr.get(value, " ")

    def __repr__(self):
        rows = []
        for i in range(self.num_rows):
            values = self.getRow(i)
            rows.append(
                "|{0}|".format("|".join(map(self.valueToStr, values))))

        return "\n".join(reversed(rows))

    def play(self, player, col: int) -> int:
        """Player `player` puts a token at column `col`.
        Modifies the board and returns the row at which the token landed.
        """
        if col >= self.num_cols or col < 0:
            return -1

        row = self.getHeight(col)
        if row < self.num_rows:
            self.board[col][row] = player

        return row

    def unplay(self, col: int) -> int:
        """Player `player` puts a token at column `col`.
        Modifies the board and returns the row at which the token landed.
        """
        if col >= self.num_cols or col < 0:
            return -1

        row = self.getHeight(col)-1
        if row < self.num_rows:
            self.board[col][row] = 0

        return row

    def getHeight(self, col):
        """Returns the current height on the column `col`"""
        row = self.num_rows
        for i in range(self.num_rows):
            if self.board[col][i] == 0:
                row = i
                break
        return row

    def getPossibleColumns(self):
        """Returns all the possible columns that can be played"""
        result = []
        for col in range(self.num_cols):
            row = self.getHeight(col)
            if row < self.num_rows:
                result.append(col)

        return result

    def getRow(self, row):
        return list(map(lambda x: x[row], self.board))

    def getCol(self, col):
        return self.board[col]

    def getDiagonal(self, up, shift):
        """
         Down: x + y = shift
         Up: x - y = shift
        """
        result = []
        if up:
            for col in range(shift, self.num_cols):
                pos = (col, col - shift)
                if pos in self:
                    result.append(self[pos])
        else:
            for col in range(shift + 1):
                pos = (col, shift - col)
                if pos in self:
                    result.append(self[pos])
        return result

    def isFull(self):
        numEmpty = 0
        for column in self.board:
            for value in column:
                numEmpty += int(value == 0)

        return numEmpty == 0
    
    def win(self):
        cols = self.num_cols
        rows = self.num_rows
        score=0
        L = []
        for i in range(cols):
            L.append(self.getCol(i))

        for j in range(rows):
            L.append(self.getRow(j))

        for k in range(cols):
            L.append(self.getDiagonal(up=False, shift=k))
            L.append(self.getDiagonal(up=True, shift=k))
            
        for element in L:
            long_seq = longest(element)[1]
            if long_seq == 4:
                return True
        return False
            

