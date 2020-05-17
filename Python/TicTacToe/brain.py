import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from tqdm import tqdm
import tqdm as tqdm
import numpy as np
import engine
import time


class MCTicTacToe:

    N_Training_Rounds = 15750
    verbose = False

    def __init__(self, verbosity):
        # Populate a game tree for deriving the probability of every possible branch?
        # There cannot be more than 5 levels of play in Tic tac toe because there are
        # two players, 9 squares and each player takes turns moving.
        """ Keys are tile # and value is probability that this move led to a winning game """
        w0 = 0.0    # I think these should be initialized at zero actually
        self.weights_move_1 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_2 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_3 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_4 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_5 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_6 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_7 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weights_move_8 = {1: w0,2: w0,3: w0,4: w0,5: w0,6: w0,7: w0, 8: w0, 9: w0}
        self.weight_table = {1: self.weights_move_1,
                             2: self.weights_move_2,
                             3: self.weights_move_3,
                             4: self.weights_move_4,
                             5: self.weights_move_5,
                             6: self.weights_move_6,
                             7: self.weights_move_7,
                             8: self.weights_move_8}
        # Now can I use this labeled game history to populate a Monte Carlo Search Tree?
        self.verbose = verbosity
        games, win_loss, game_sizes = self.create_initial_game_tree()

    # TODO: break into more sub functions?
    def create_initial_game_tree(self):
        """
        --------------------------------------------------------------------------------
        CREATE_GAME_TREE                                            TODO: Fill this in
        --------------------------------------------------------------------------------
        http://www.mathrec.org/old/2002jan/solutions.html
        *  47,952  games end with three in a row after seven moves
        *  54,720  games which end with three in a row before the eighth move
        * 255,168  games where one player completes three in a row or the board is full
        """
        if self.verbose:
            print '\033[1m====\t\033[31m\033[1mStarting Self-Play\033[0m\033[1m\t====\033[0m'
        n_moves = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}  # game length
        distribution = {'X': 0, 'O': 0, '': 0}
        tic = time.time()

        games = {'Wins': [], 'Loss': []}
        game_index = 0
        for i in tqdm.tqdm(range(self.N_Training_Rounds)):
            winner, state, nm = self.self_play(False)
            if winner=='X':
                games['Wins'].append(state)
            else:
                games['Loss'].append(state)
            n_moves[nm + 1] += 1
            distribution[winner] += 1
            game_index += 1

        if self.verbose:
            self.show_self_play_stats(distribution, n_moves, self.N_Training_Rounds, tic)

        # Ok Now Let's build the Monte Carlo Tree
        for round in games['Wins']:
            # Update self.weights based on what happens in each winning game
            self.learn_from_game(round)
        # Re-adjust the weights based on the losses
        if self.verbose:
            self.reveal_internal_state()

        # AI Win Rate
        win_rate = distribution['X']/float(distribution['O'] + distribution['X']+ distribution[''])
        return games, distribution, n_moves

    def self_play(self, show):
        """
        play a random game of tic tac toe to populate game tree
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

    def show_self_play_stats(self, distr, nm, nt, t):
        winX = 100.0 * (distr['X'] / float(nt))
        winO = 100.0 * (distr['O'] / float(nt))
        draw = 100.0 * (distr[''] / float(nt))

        print '[*] Finished Running %d Trials [%ss Elapsed]' % (nt, str(time.time() - t))
        print '\033[1m\033[32mX\033[0m won %d/%d Games [%s percent]' % (distr['X'], nt, str(winX))
        print '\033[1m\033[34mO\033[0m won %d/%d Games [%s percent]' % (distr['O'], nt, str(winO))
        print 'Tied %d/%d Games [%s percent]' % (distr[''], nt, str(draw))
        print 'Game Length Distribution: '
        print nm
        print '\033[1m' + '=' * 60 + '\033[0m'

    def learn_from_game(self, moves):
        assign_weights = {1:self.weights_move_2,
                          2:self.weights_move_3,
                          3:self.weights_move_4,
                          4:self.weights_move_5,
                          5:self.weights_move_6,
                          6:self.weights_move_7,
                          7:self.weights_move_8,
                          }
        n_steps = len(moves)
        # Determine where the first move made
        [dx1, dy1] = self.find_cell_moved(np.zeros((3, 3)), moves[0])
        mv1 = np.array(engine.TicTacToe.where)[dx1, dy1]
        self.weights_move_1[mv1] += 1
        # Determine the other moves made
        for step in range(1,n_steps):
            try:
                [dnx, dny] = self.find_cell_moved(moves[step - 1], moves[step])
                mvN = np.array(engine.TicTacToe.where)[dnx, dny]
                assign_weights[step][mvN] += 1
            except ValueError:
                # Game ended with a tie, so there were no changes?
                break

    def find_cell_moved(self, last_state, new_state):
        diff_row_1 = new_state[0,:] - last_state[0,:]
        diff_row_2 = new_state[1,:] - last_state[1,:]
        diff_row_3 = new_state[2,:] - last_state[2,:]
        # Any non zero is new, equal to 1 is an X
        f1 = np.where(diff_row_1 == 1)[0]
        f2 = np.where(diff_row_2 == 1)[0]
        f3 = np.where(diff_row_3 == 1)[0]
        if len(f1):
            moved = [f1[0], 0]
        elif len(f2):
            moved = [f2[0], 1]
        elif len(f3):
            moved = [f3[0], 2]
        else:
            # Prob an error? Nothing changed
            moved = []
        return moved

    def find_opponent_moved(self, last_state, new_state):
        diff_row_1 = new_state[0,:] - last_state[0,:]
        diff_row_2 = new_state[1,:] - last_state[1,:]
        diff_row_3 = new_state[2,:] - last_state[2,:]
        # Any non zero is new, equal to -1 is a O
        f1 = np.where(diff_row_1 == -1)[0]
        f2 = np.where(diff_row_2 == -1)[0]
        f3 = np.where(diff_row_3 == -1)[0]
        if len(f1):
            moved = [f1[0], 0]
        elif len(f2):
            moved = [f2[0], 1]
        elif len(f3):
            moved = [f3[0], 2]
        else:
            # Prob an error? Nothing changed
            moved = []
        return moved

    def reveal_internal_state(self):
        print '='*10+' WEIGHTS '+'='*10
        print self.weights_move_1
        print self.weights_move_2
        print self.weights_move_3
        print self.weights_move_4
        print self.weights_move_5
        print self.weights_move_6
        print self.weights_move_7
        print self.weights_move_8



if __name__ == '__main__':
    game_tree = MCTicTacToe(True)


