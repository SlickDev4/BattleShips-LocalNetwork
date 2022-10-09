import pygame
from variables import *
from widgets import Square
from random import sample


class Game:
    def __init__(self):
        self.initialized = False
        self.players_connected = [False, False]
        self.squares_initialized = False
        self.squares_need_update = [False, False]
        self.someone_won = False

        self.p1_squares = [[], []]
        self.p2_squares = [[], []]

        self.ships = [20, 20]
        self.ships_killed = [0, 0]
        self.moves_left = [50, 50]

        self.ships_indices = [sample(range(1, 101), 20), sample(range(1, 101), 20)]

        self.turn = 0

        self.squares_init()

    def is_initialized(self):
        return self.initialized

    def players_are_connected(self):
        if False in self.players_connected:
            return False
        return True

    def connect_player(self, player):
        """
            This method is connecting the players
                                                    """
        self.players_connected[player] = True

    def squares_init(self):
        """
            This is a small algorythm that is creating the squares and the pattern - it is not the best pattern,
            as the ships are placed totally random, and they are not like real ships.
                                                                                     """

        for idx in range(2):
            # reversing the squares and creating them 4 times instead of 2 just to
            # send them properly to the players depending on their id and position

            if idx == 0:
                square_pos = [[28, 178, 41, 41], [728, 178, 41, 41]]
            else:
                square_pos = [[728, 178, 41, 41], [28, 178, 41, 41]]

            for p in range(2):
                for sq in range(1, 101):

                    # color is GRAY if the square is not a ship
                    color = GRAY
                    # but if it is, we change the color to ORANGE
                    if sq in self.ships_indices[p]:
                        color = ORANGE

                    # initializing the square
                    square = Square(color, *square_pos[p])

                    # if it is ORANGE, we set its ship property to True
                    if color == ORANGE:
                        square.is_ship_ = True

                    # if the index is 0, we append the player 1 squares
                    if idx == 0:
                        self.p1_squares[p].append(square)
                    # otherwise, we append the player 2 squares
                    else:
                        self.p2_squares[p].append(square)

                    # we are changing the position for every square on every iteration
                    square_pos[p][1] += 44

                    # if we hit 10 squares we reset the position and go 1 square to the right and repeat
                    if sq % 10 == 0:
                        square_pos[p][1] = 178
                        square_pos[p][0] += 44

        # here we are reversing the squares for player 2 as their screen will be reversed as well
        self.p2_squares = [self.p2_squares[1], self.p2_squares[0]]

        # here we are turning all the enemy ORANGE squares to GRAY, so they won't be visible but since
        # they have their property is_ship to True, we will recognize them
        for sq1, sq2 in zip(self.p1_squares[1], self.p2_squares[1]):
            sq1.color = GRAY
            sq2.color = GRAY

    def get_squares(self, player):
        """
            This method is giving the squares to the client depending on the player id
                                                                                        """
        if player == 0:
            return self.p1_squares
        return self.p2_squares

    def get_turn(self):
        return self.turn

    def update_squares(self, player, hit, idx):
        """
            This method is updating the squares depending on the player if they hit or missed
                                                                                                """

        # if the player hit - we make the square blue and a little smaller
        # we also assign the is_dead to True, so it can't be hovered or clicked anymore,
        # we are decrementing the enemy ships and incrementing our killed ships
        # additionally if the player hit, it is still their turn
        if hit == "hit":
            self.p1_squares[player-1][idx].color = (0, 0, 255)
            self.p1_squares[player-1][idx].is_dead_ = True
            self.p1_squares[player-1][idx].width = 25
            self.p1_squares[player-1][idx].height = 25
            self.p1_squares[player-1][idx].x += 5
            self.p1_squares[player-1][idx].y += 5

            self.p2_squares[player][idx].color = (0, 0, 255)
            self.p2_squares[player][idx].is_dead_ = True
            self.p2_squares[player][idx].width = 25
            self.p2_squares[player][idx].height = 25
            self.p2_squares[player][idx].x += 5
            self.p2_squares[player][idx].y += 5

            self.ships[player - 1] -= 1
            self.ships_killed[player] += 1

        # if the player missed, we are making the square black and a lot smaller, centered in the middle
        # as hit, we are assigning the is_dead to True so this can't be hovered or clicked as well
        # additionally, we change the player turn as they missed
        else:
            self.p1_squares[player-1][idx].color = (0, 0, 0)
            self.p1_squares[player-1][idx].is_dead_ = True
            self.p1_squares[player-1][idx].width = 10
            self.p1_squares[player-1][idx].height = 10
            self.p1_squares[player-1][idx].x += 15
            self.p1_squares[player-1][idx].y += 15

            self.p2_squares[player][idx].color = (0, 0, 0)
            self.p2_squares[player][idx].is_dead_ = True
            self.p2_squares[player][idx].width = 10
            self.p2_squares[player][idx].height = 10
            self.p2_squares[player][idx].x += 15
            self.p2_squares[player][idx].y += 15

            self.turn = 1 if player == 0 else 0

        # in both cases, we are decrementing the moves left
        # and signaling the server that the squares need an update
        self.moves_left[player] -= 1
        self.squares_need_update = [True, True]

    def reset(self):
        """
            This method resets the game when the player leaves after winning, losing or being tied
            We are actually using this in order to stop the end game checks in the client, but
            when both players disconnect, the game object is destroyed, and it will be initialized
            again when both players reconnect to the game.
                                                                                                    """

        self.initialized = False
        self.players_connected = [False, False]
        self.squares_initialized = False
        self.squares_need_update = [False, False]
        self.someone_won = False

        self.p1_squares = [[], []]
        self.p2_squares = [[], []]

        self.ships = [20, 20]
        self.ships_killed = [0, 0]
        self.moves_left = [50, 50]

        self.ships_indices = [sample(range(1, 101), 20), sample(range(1, 101), 20)]

        self.turn = 0

        self.squares_init()
