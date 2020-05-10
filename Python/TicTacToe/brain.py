import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from tqdm import tqdm
import tqdm as tqdm
import numpy as np
import engine
import time


class MCTicTacToe:

    def __init__(self):
        # Populate a game tree for deriving the probability of every possible branch?
        # There cannot be more than 5 levels of play in Tic tac toe because there are
        # two players, 9 squares and each player takes turns moving.
        """ Keys are tile # and value is probability that this move led to a winning game """
        w0 = 1/9.0
        self.weights_move_1 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}
        self.weights_move_2 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}
        self.weights_move_3 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}
        self.weights_move_4 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}
        self.weights_move_5 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}
        self.weights_move_6 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}
        self.weights_move_7 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0,8: w0,9: w0}

    def self_play(self, show):
        """

        :param show:
        :return:
        """
        botA = 'X'
        botB = 'O'
        winner = ''
        board = engine.TicTacToe(botA)
        move_ct_a = 0
        move_ct_b = 0
        '''
        Training from Bot A perspective
        '''
        history = []
        while board.running:
            board.find_random_move()
            move_ct_a += 1
            history.append(np.array(board.board))
            if board.choices[int(board.check_for_winner())] == botA:
                # BOT_A Wins
                board.running = False
                winner = botA
                # Save Win States
                if show:
                    print '[*] Bot A Wins!\n'
                    print board.show(True)

            moved, random_move = board.seek_random_move(board, botB)

            if not moved:
                board.running = False

            move_ct_b += 1

            if board.choices[int(board.check_for_winner())] == botB:
                # BOT_B Wins
                board.running = False
                winner = botB
                if show:
                    print '[*] Bot B Wins\n!'
                    print board.show(True)

        # print 'FINISHED'
        # gameplay = board.game

        return winner, history, (move_ct_a+move_ct_b)/2


if __name__ == '__main__':
    distribution = {'X': 0, 'O': 0, '':0}
    n_moves = {3:0,4:0,5:0,6:0,7:0,8:0} # Indexed from zero
    tic = time.time()
    n_trials = 1
    # I think there 15120 possible games of Tic Tac Toe? (9*8*7*6*5=15,120)
    # Not quite: http://www.mathrec.org/old/2002jan/solutions.html
    """
    *  47,952  games end with three in a row after seven moves
    *  54,720  games which end with three in a row before the eighth move
    * 255,168  games where one player completes three in a row or the board is full
    """
    print '\033[1m====\t\033[31m\033[1mStarting Training\033[0m\033[1m\t====\033[0m'

    games = {'Wins': [], 'Loss': []}
    game_index = 0
    for i in tqdm.tqdm(range(n_trials)):
        winner, state, nm = MCTicTacToe().self_play(False)
        if winner:
            games['Wins'].append(state)
        else:
            games['Loss'].append(state)
        n_moves[nm+1] += 1
        distribution[winner] += 1
        game_index += 1

    winX = 100.0*(distribution['X']/float(n_trials))
    winO = 100.0*(distribution['O']/float(n_trials))
    draw = 100.0*(distribution['']/float(n_trials))

    print '[*] Finished Running %d Trials [%ss Elapsed]' % (n_trials, str(time.time()-tic))
    print '\033[1m\033[32mX\033[0m won %d/%d Games [%s percent]' % (distribution['X'], n_trials, str(winX))
    print '\033[1m\033[34mO\033[0m won %d/%d Games [%s percent]' % (distribution['O'], n_trials, str(winO))
    print 'Tied %d/%d Games [%s percent]' % (distribution[''], n_trials, str(draw))
    print 'Game Length Distribution: '
    print n_moves
    print '\033[1m'+'='*60+'\033[0m'

    # Now can I use this labeled game history to populate a Monte Carlo Search Tree?


