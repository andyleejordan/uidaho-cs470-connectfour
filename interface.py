import argparse
import sys

from error import *

class Interface:
    def __init__(self, colors):
        self.colors = colors

    def printBoard(self): raise NotImplementedError
    def askMove(self): raise NotImplementedError

class GUI(Interface):
    def __init__(self, colors):
        raise NotImplementedError

class CLI(Interface):
    def __init__(self, colors):
        super().__init__(colors)
        self.ask_string = "Player {}, in which column would you like to play? "

    def eatargs(self):
        parser = argparse.ArgumentParser(description='Play Connect Four!')
        parser.add_argument('--versus', dest='players', action='store_const',
                const=['Human', 'Human'], help='Play as two Humans!')
        parser.add_argument('--solo', dest='players', action='store_const',
                const=['Human', 'Computer'], help='Play as two Humans!')
        parser.add_argument('--auto', dest='players', action='store_const',
                const=['Computer', 'Computer'], help='Play as two Computers!')
        options = parser.parse_args()
        if options.players is None:
            options.players = ['Human', 'Human']

        return options.players

    def _getSymbol(self, color):
        if color == self.colors[0]:
            return '#'
        if color == self.colors[1]:
            return '*'

    def newGame(self, players, board):
        welcome_string = "Welcome players: {} is '{}', and {} is '{}'."
        print(welcome_string.format(
            players[0].color, self._getSymbol(players[0].color),
            players[1].color, self._getSymbol(players[1].color)))
        board.printBoard()
        print('Your columns are 0 to 6, left to right.')

    def endGame(self, winner, board):
        if winner is None:
            print('It was a draw!')
        else:
            print('Player {} won!'.format(winner.color))
        board.printBoard()

    def printBoard(self, the_board):
        print()
        for row in range(the_board.height-1, -1, -1):
            print('|', end='')
            for column in range(the_board.width):
                space = the_board.board[column][row]
                if space == self.colors[0]:
                    print(self._getSymbol(self.colors[0]), end='')
                if space == self.colors[1]:
                    print(self._getSymbol(self.colors[1]), end='')
                if space is None:
                    print(' ', end='')
                print('|', end='')
            print()
        print('|' + '|'.join(str(i) for i in range(the_board.width)) + '|')
        print()

    def _exit(self):
            print('Goodbye cruel world.')
            sys.exit(0)

    def askMove(self, color):
        try:
            input_ = input(self.ask_string.format(color))
        except KeyboardInterrupt:
            self._exit()
        print()
        if input_ == 'exit':
            self._exit()
        try:
            return int(input_)
        except:
            raise InvalidMoveError
