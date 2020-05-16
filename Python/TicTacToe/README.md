# Tic Tac Toe AI From Scratch
I came across the concept of Monte Carlo Search Trees, and it just seemed so effective
and interesting I wanted to try and implement it for myself. So I figured a simple game
like Tic Tac Toe would be a good thing to try and tackle with it. 

So far I'm using random self play. Looking at the games that are Wins I count the moves 
used, creating a kind of histogram of options that led to victory. This alone has been
interesting because with only a couple thousand games it quickly finds the best strategy
as being to move to the center. 

![raw_counts](https://raw.githubusercontent.com/scott-robbins/ByteClub/master/Python/TicTacToe/self-play.png)