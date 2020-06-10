# Tic Tac Toe AI From Scratch
I came across the concept of Monte Carlo Search Trees, and it just seemed so effective
and interesting I wanted to try and implement it for myself. So I figured a simple game
like Tic Tac Toe would be a good thing to try and tackle with it. 

So far I'm using random self play. Looking at the games that are Wins I count the moves 
used, creating a kind of histogram of options that led to victory. This alone has been
interesting because with only a couple thousand games it quickly finds the best strategy
as being to move to the center. 

![raw_counts](https://raw.githubusercontent.com/scott-robbins/ByteClub/master/Python/TicTacToe/self-play.png)

```
>>> import brain, engine, game
>>> import numpy as np
>>>
>>> board = engine.TicTacToe('X')
>>> ai = brain.MCTicTacToe(True)
```

Deciding the best move with the Monte Carlo tree is about selecting the highest probability
the table corresponding to the turn number.

```
turn = 1
>>> cell = {1: [0, 0], 2: [1, 0], 3: [2, 0],
            4: [0, 1], 5: [1, 1], 6: [2, 1],
            7: [0, 2], 8: [1, 2], 9: [2, 2]}
>>> odds = ai.weight_table[turn]
>>> best_cell = np.where(np.array(odds.values())==np.array(odds.values()).max())[0][0]+1
```
*Plus one because the array of keys is indexed from zero but moves are indexed from one.* 

However, aside from making the the first move we will have to also only consider tiles where
our opponent hasn't placed a mark.

```
>>> best_cell = np.where(np.array(odds.values())==np.array(odds.values()).max())[0][0]

```