import numpy as np
import brain
import sys
import os


class TicTacToe:
    tiles = {1: [0,0], 2: [1,0], 3: [2,0],
             4: [0,1], 5: [1,1], 6: [2,1],
             7: [0,2], 8: [1,2], 9: [2,2]}
    where = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    team = ''
    running = False
    board = [[]]
    game = []

    def __init__(self, ai_team):
        if ai_team in ['X', 'O']:
            self.team = ai_team
        else:
            print '[!!] AI must be either X or O'
            exit()
        self.choices = {-1: 'O', 0: ' ', 1: 'X'}
        self.lookup = {'O': -1, 'X': 1, ' ': 0}
        self.running = True
        self.set_board()


    def set_board(self):
        """
        Game board is 3x3 of 0s (empty spaces)
        An X is +1, and and O is -1
        :return:
        """
        self.board = np.zeros((3, 3))
        self.game.append(np.copy(self.board))

    def show(self, showMoves):
        """
        Produce a string representation of the
        TicTacToe board.
        :param showMoves:
        :return:
        """
        rows = ['1 4 7', '2 5 8', '3 6 9']
        out = '  board | moves\n'+'='*15+'\n'
        n = 0
        for row in self.board:
            r = ''
            for c in row:
                if c not in self.choices.keys():
                    print '[!!] Illegal Board'
                else:
                    r += self.choices[c] + ' '
            if showMoves:
                out += r + ' \t| '+rows[n]+'\n'
            else:
                out += r + '\n'
            n += 1
        out += '='*15
        return out

    def set_cell(self, piece, move):
        if piece in self.tiles.keys():
            [x, y] = self.tiles[piece]
            if self.board[x, y] != 0:
                print '[!!] Cannot move to [%d,%d] because its taken' % (x, y)
                print self.show(False)
                return False
            elif move in self.choices.keys():
                self.board[x,y] = move
                self.game.append(np.copy(self.board))
                return True
            else:
                print '[!!] %d is not a legal choice' % move
                return False
        else:
            return False

    def find_random_move(self):
        # for now this is random
        moved = False
        guessed = []
        while not moved:
            random_guess = np.random.random_integers(1,9,1)[0]
            [x,y] = self.tiles[random_guess]
            if self.board[x,y] == 0:
                self.board[x,y] = self.lookup[self.team]
                moved = True
            else:
                guessed.append(random_guess)
            if len(guessed) >= 9:
                # print '[!!] No Legal Moves Available'
                return False, []
        return True, random_guess

    @staticmethod
    def seek_random_move(board, team):
        cell = {1: [0, 0], 2: [1, 0], 3: [2, 0],
                4: [0, 1], 5: [1, 1], 6: [2, 1],
                7: [0, 2], 8: [1, 2], 9: [2, 2]}
        moved = False
        guess = []
        while not moved:
            random_guess = np.random.random_integers(1,9,1)[0]
            [x,y] = cell[random_guess]
            if board.board[x,y] == 0:
                board.board[x,y] = board.lookup[team]
                moved = True
            else:
                guess.append(random_guess)
            if len(guess) >= 9:
                return False, []
        return True, random_guess

    def consider_move(self, board,ai, turn_no):
        # pull the probabilities for each square in monte carlo search
        # tree for which move has the most wins associated with a choice
        cell = {1: [0, 0], 2: [1, 0], 3: [2, 0],
                4: [0, 1], 5: [1, 1], 6: [2, 1],
                7: [0, 2], 8: [1, 2], 9: [2, 2]}
        odds = ai.weight_table[turn_no]
        moved = False
        best_cell = np.where(np.array(odds.values())==np.array(odds.values()).max())[0][0]+1
        [gx,gy] = cell[best_cell]
        if board.board[gx,gy]==0:
            guessed = best_cell
        else:
            # TODO: Fix this to find next best choices, not random ones!!
            status, guessed = self.find_random_move()

        return guessed

    def check_for_winner(self):
        r1 = self.board[:, 0]
        r2 = self.board[:, 1]
        r3 = self.board[:, 2]
        c1 = self.board[0, :]
        c2 = self.board[1, :]
        c3 = self.board[2, :]
        if len(np.unique(r1)) == 1:
            return np.unique(r1)[0]
        if len(np.unique(r2)) == 1:
            return np.unique(r2)[0]
        if len(np.unique(r3)) == 1:
            return np.unique(r3)[0]
        if len(np.unique(c1)) == 1:
            return np.unique(c1)[0]
        if len(np.unique(c2)) == 1:
            return np.unique(c2)[0]
        if len(np.unique(c3)) == 1:
            return np.unique(c3)[0]
        # Now check diagonals
        [ax, ay] = self.tiles[1]; da = self.board[ax, ay]   # | x |   |   |
        [bx, by] = self.tiles[5]; db = self.board[bx, by]   # |   | x |   |
        [cx, cy] = self.tiles[9]; dc = self.board[cx, cy]   # |   |   | x |
        [ix, iy] = self.tiles[7]; di = self.board[ix, iy]   # |   |   | x |
        [jx, jy] = self.tiles[5]; dj = self.board[jx, jy]   # |   | x |   |
        [kx, ky] = self.tiles[3]; dk = self.board[kx, ky]   # | x |   |   |
        diag1 = np.unique(np.array([da, db, dc]))
        diag2 = np.unique(np.array([di, dj, dk]))
        if len(np.unique(diag1)) == 1:
            return np.unique(diag1)[0]
        if len(np.unique(diag2)) == 1:
            return np.unique(diag2)[0]
        return 0


if __name__ == '__main__':
    if len(sys.argv)<1 or 'test' in sys.argv:
        # Create the game board
        board = TicTacToe('O')
        first_move = False

        if first_move:
            board.find_random_move()  # TODO: Use a game tree + search algorithm
            print board.show(True)
        else:
            print board.show(True)
            option = int(raw_input('Enter a move: '))
            board.set_cell(option, board.lookup['X'])  # User is X by default for now

        # Start running the game loop
        while board.running:
            os.system('clear')
            if board.choices[int(board.check_for_winner())] == 'X':
                print '[*] User Wins!'
                board.running = False
                break
            ''' Let The Bot Move '''
            bot_moved, choice = board.find_random_move()  # TODO: Use a game tree + search algorithm
            winner = board.choices[int(board.check_for_winner())]
            if not bot_moved:
                print '!! [GAME OVER] !!'
                exit()

            print board.show(True)

            if winner == 'O':
                print '[*] Bot Wins!'
                board.running = False

            '''  Let the User MOve '''
            user_moved = False
            while not user_moved and board.running:
                option = int(raw_input('Enter a move: '))
                user_moved = board.set_cell(option, board.lookup['X'])
        print board.show(True)
