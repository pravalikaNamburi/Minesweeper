import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()
    
    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                continue

            board[row][col] = '*'
            bombs_planted += 1
        
        return board
    
    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)
    
    def get_num_neighbouring_bombs(self, row, col):
        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True
    
    def __str__(self):
        visible_board = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
        
        string_rep = ''
        widths = [max(len(str(visible_board[row][col])) for row in range(self.dim_size)) for col in range(self.dim_size)]

        indices_row = '    ' + '  '.join([f'{i:<{widths[i]}}' for i in range(self.dim_size)]) + '\n'

        string_rep += indices_row
        string_rep += '   ' + '-' * (len(indices_row) - 4) + '\n'

        for i in range(self.dim_size):
            row_str = f'{i:<2} | ' + ' | '.join([f'{visible_board[i][j]:<{widths[j]}}' for j in range(self.dim_size)]) + ' |\n'
            string_rep += row_str

        string_rep += '  ' + '-' * (len(indices_row) - 4) + '\n'
        
        return string_rep

def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)
    safe = True

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)

        user_input = input("Where do you like to dig? (row,col): ")
        try:
            row, col = map(int, re.split(r'\D+', user_input))
            if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
                raise ValueError("Invalid location.")
        except ValueError:
            print("Invalid input, try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("Congrats! YOU WON!")
    else:
        print("GAME OVER")
        board.dug = {(r, c) for r in range(board.dim_size) for c in range(board.dim_size)}
        print(board)

if __name__ == "__main__":
    play()
