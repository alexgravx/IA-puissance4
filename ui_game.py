import tkinter

from board import Board
from game import Game


class UIGame(Game):
    """Play the connect 4 game, but in a Tkinter GUI"""
    def __init__(self, player1, player2, dbg=None):
        super().__init__(player1, player2, verbose=False)
        self.tk = tkinter.Tk()
        self.width = 700
        self.height = 600
        self.timeout = 2 * 1000
        self.cellH = self.height / self.board.num_rows
        self.cellW = self.width / self.board.num_cols

        self.labels = []
        for k, player in enumerate(self.players):
            self.labels.append(tkinter.Label(
                self.tk, text=player.name, fg=self.getColor(player.color),
                font=("Helvetica", 16)))
            self.labels[-1].grid(row=0, column=k)

        self.info = tkinter.StringVar()
        self.infoLabel = tkinter.Label(
            self.tk, textvariable=self.info, font=("Helvetica", 16))
        self.infoLabel.grid(row=1, column=0, columnspan=2)

        if dbg:
            self.infoLabel = tkinter.Label(
                self.tk, text=dbg, font=("Helvetica", 14))
            self.infoLabel.grid(row=0, column=2, rowspan=3, sticky='n')

        self.canvas = tkinter.Canvas(
            height=self.height, width=self.width)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.grid(row=2, column=0, columnspan=2)

        self.reset()

        # A bit to make sure to stop when it's over.
        self.over = False
        # Start the game if the player to start is not Human
        self.run()

        self.tk.mainloop()

    @staticmethod
    def getColor(value):
        return 'red' if value == 1 else 'blue'

    def renderOne(self, i, j):
        x = self.cellW * i
        y = self.height - self.cellH * j
        color = self.getColor(self.board[i, j])
        self.canvas.create_oval(
            x, y, x + self.cellW, y - self.cellH, fill=color)

    def render(self, board):
        for i in range(board.num_cols):
            for j in range(board.num_rows):
                if board[i, j] != 0:
                    self.renderOne(i, j)

    def run(self):
        if self.over:
            return

        player = self.players[self.currPlayer]
        if player.HUMAN:
            return

        try:
            col = player.getColumn(self.board)
            if 0 <= col < self.board.num_cols:
                self.play(col)
        except:
            self.mayMakeCurrentPlayerLoose()

    def click(self, event):
        """Reponse to a click event, for human player only."""
        player = self.players[self.currPlayer]
        if player.HUMAN:
            col = int(event.x / self.cellW)
            self.play(col)

    def play(self, col):
        """The current player puts a token on the column given as input"""
        if self.over:
            return

        player = self.players[self.currPlayer]
        row = self.board.play(player.color, col)
        pos = (col, row)

        # AI mistake ? not good. You loose
        if pos not in self.board:
            self.mayMakeCurrentPlayerLoose()
            return

        self.renderOne(col, row)
        self.currPlayer = (self.currPlayer + 1) % 2
        self.winner = self.getWinner(pos)
        if not self.handleEnd():
            self.tk.after(20, self.run)

    def mayMakeCurrentPlayerLoose(self):
        player = self.players[self.currPlayer]
        if not player.HUMAN:
            self.winner = self.players[(self.currPlayer + 1) % 2]
            self.over = True
            self.handleEnd()

    def handleEnd(self):
        if not self.isOver() and not self.over:
            return False

        text = "It's a draw!"
        if self.winner is not None:
            text = "{0} ({1}) wins!".format(
                self.winner.name, Board.valueToStr(self.winner.color))
        self.info.set(text)
        self.over = True
        self.tk.after(self.timeout, self.tk.destroy)
        return True
