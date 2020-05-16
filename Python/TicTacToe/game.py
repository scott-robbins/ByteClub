import numpy as np
import engine
import brain
import sys
import os


def choose_side():
    selected = False
    team = {'X': False, 'O': False}
    print '[*] Please select a team for TicTacToe'
    while not selected:
        print 'Enter X or O:'
        opt = raw_input('Enter a Selection:').upper()
        if opt not in team.keys():
            print '[!!] That is not a good choice'
        else:
            selected = True
            team[opt] = True
    bteam = team.keys()[np.where(np.array(team.values()) == False)[0][0]]
    print '[*] Ok. So bot will be playing as %s' % bteam
    return bteam, opt


def choose_order():
    selected = False
    first_move = False
    while not selected:
        print '[*] Do you want the first move (Y/N) ?: '
        opt = raw_input('Enter a selection: ').upper()
        if opt == ('Y' or 'YES'):
            first_move = True
            selected = True
        elif opt == ('Y' or 'NO'):
            first_move = False
            selected = True
        else:
            print 'Bad choice'
    return first_move


def get_move_from_user(g):
    print g.show(True)
    chosen = False
    while not chosen:
        mv = int(raw_input('Enter a move [1-9]: '))
        if mv in np.array([1,2,3,4,5,6,7,8,9]):
            chosen = True
        else:
            print '[!!] Bad choice'
    return mv


def bot_first_game_loop(game1, ai_team, my_team):
    winner = {'ai': False, 'me': False}
    while game1.running:
        # Let Bot move
        game1.find_random_move()
        if game1.choices[int(game1.check_for_winner())] == ai_team:
            print '[*] Bot Wins!'
            winner['ai'] = True
            game1.running = False
            break
        # Let user move
        option = get_move_from_user(game1)
        game1.set_cell(option, game1.lookup[my_team])
        # Check if user won
        if game1.choices[int(game1.check_for_winner())] == my_team:
            print '[*] User Wins!'
            winner['me'] = True
            game1.running = False
            break
    print '! ! ! GAME OVER ! ! !'
    return winner, game1


def user_first_game_loop(game, ai_team, my_team):
    winner = {'ai': False, 'me': False}
    # print game.show(True)
    while game.running:
        # Let user move
        option = get_move_from_user(game)
        game.set_cell(option, game.lookup[my_team])
        # Check if user won
        if game.choices[int(game.check_for_winner())] == my_team:
            print '[*] User Wins!'
            winner['me'] = True
            game.running = False
            break
        # Let Bot move
        game.find_random_move()
        if game.choices[int(game.check_for_winner())] == ai_team:
            print '[*] Bot Wins!'
            winner['ai'] = True
            game.running = False
            break
    print '! ! ! GAME OVER ! ! !'
    return winner, game


def play_against_ai(game, ai_team, my_team):
    winner = {'ai': False, 'me': False}
    turn = 1
    ideas = brain.MCTicTacToe(False)

    while game.running:
        # Let Bot Move
        option = game.consider_move(game, ideas, turn)
        game.set_cell(option, game.lookup[ai_team])

        # check if bot won
        if game.choices[int(game.check_for_winner())] == ai_team:
            print '[*] Bot Wins!'
            winner['ai'] = True
            game.running = False
            break

        # Let user move
        option = get_move_from_user(game)
        game.set_cell(option, game.lookup[my_team])

        # Check if user won
        if game.choices[int(game.check_for_winner())] == my_team:
            print '[*] User Wins!'
            winner['me'] = True
            game.running = False
            break

    print '! ! ! GAME OVER ! ! !'
    return winner, game


def run_game():
    bot_team, ppl_team = choose_side()
    # Create Game Board
    board = engine.TicTacToe(bot_team)

    if 'play' in sys.argv:
        play_against_ai(board, bot_team, ppl_team)
    else:
        result, board = user_first_game_loop(board, bot_team, ppl_team)

    # Show how the game went
    for state in board.game:
        print np.array(state).astype(np.str)


if __name__ == '__main__':
    run_game()




