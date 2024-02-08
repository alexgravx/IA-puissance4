from player import Player
from utils import longest
from mesure_time import timeit
import copy
import random

class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max or alpha
    beta search to """


    def __init__(self):
        super().__init__()
        self.name = "Gravlax-AI"
        
    def heuristique(self, board):
        cols = board.num_cols
        rows = board.num_rows
        score=0
        L = []
        for i in range(cols):
            L.append(board.getCol(i))

        for j in range(rows):
            L.append(board.getRow(j))

        for k in range(cols):
            L.append(board.getDiagonal(up=False, shift=k))
            L.append(board.getDiagonal(up=True, shift=k))
            
        for element in L:
            long_elem,long_seq = longest(element)
            score += (long_seq==4 and long_elem==self.color) - (long_seq==4 and long_elem==-self.color)
            score += 0.1*(long_seq==3 and long_elem==self.color)- 0.1*(long_seq==3 and long_elem==-self.color)
        
        return score
    
    def win(self, board):
        cols = board.num_cols
        rows = board.num_rows
        L = []
        for i in range(cols):
            L.append(board.getCol(i))

        for j in range(rows):
            L.append(board.getRow(j))

        for k in range(cols):
            L.append(board.getDiagonal(up=False, shift=k))
            L.append(board.getDiagonal(up=True, shift=k))
            
        for element in L:
            long_elem, long_seq = longest(element)
            if long_seq >= 4:
                return long_elem
        return 0
    
    def MaxScore(self, board, alpha, beta, profondeur, max_profondeur=6):
        if profondeur == max_profondeur:
            score = self.heuristique(board)
            return score
        winner = self.win(board)
        if winner == self.color:
            return 1000
        if winner == -self.color:
            return -1000
        columns = board.getPossibleColumns()
        profondeur += 1
        for i in columns:
            board_tour = copy.deepcopy(board)
            board_tour.play(self.color, i)
            alpha = max(alpha, self.MinScore(board_tour, alpha, beta, profondeur))
            if alpha >= beta:
                return beta
        return alpha
    
    def MinScore(self, board, alpha, beta, profondeur, max_profondeur=6):
        if profondeur == max_profondeur:
            score = self.heuristique(board)
            return score
        winner = self.win(board)
        if winner == self.color:
            return 1000
        if winner == -self.color:
            return -1000
        columns = board.getPossibleColumns()
        profondeur += 1
        for i in columns:
            board_tour = copy.deepcopy(board)
            board_tour.play(-self.color, i)
            beta = min(beta, self.MaxScore(board_tour, alpha, beta, profondeur))
            if alpha >= beta:
                return alpha
        return beta
    
    def getColumn(self, board):
        columns = board.getPossibleColumns()
        L_scores = []
        for i in columns:
            board_tour = copy.deepcopy(board)
            board_tour.play(self.color, i)
            score = self.MinScore(board_tour, -1000, 1000, 0)
            L_scores.append(score)
        max_index = [i for i in range(len(L_scores)) if L_scores[i] == max(L_scores)]
        if len(max_index) > 1:
            #return columns[max_index[len(max_index)//2]]
            return columns[random.choice(max_index)]
        else:
            return columns[max_index[0]]

