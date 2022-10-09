import pygame
from variables import *
from network import Network
from widgets import Line, Square
pygame.font.init()

# window initialization
width, height = 1200, 650
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle Ships")

# background images
bg = pygame.transform.scale(pygame.image.load('assets/bg.jpg'), (1200, 650))
game_bg = pygame.transform.scale(pygame.image.load("assets/game_bg.jpg"), (1200, 650))


def is_my_turn(player, game):
    """
        This function is checking if it is the player's turn
                                                             """

    if (player == 0 and game.get_turn() == 0) or (player == 1 and game.get_turn() == 1):
        return True
    return False


def attack_enemy(squares):
    """
        This function is attacking the enemy and is checking whether the player hit a ship or missed
                                                                                                    """

    attacked_index = ''
    for square in squares[1]:
        if square.color == RED:
            attacked_index = squares[1].index(square)

    if attacked_index == '':
        return ['ignore', attacked_index]
    else:
        if squares[1][attacked_index].is_ship() and not squares[1][attacked_index].is_dead():
            return ["hit", attacked_index]
        return ["miss", attacked_index]


def draw_menu_screen(win, mouse_pos):
    """
        This function is drawing the menu screen - background and buttons
                                                                            """

    win.blit(bg, (0, 0))

    for button in menu_buttons:
        if button.is_hovered(mouse_pos):
            button.color = GREEN
            button.text_color = BLACK
        else:
            button.color = BLACK
            button.text_color = WHITE
        button.draw(win)


def draw_game_screen(win, player, squares, mouse_pos, game):
    """
        This function is drawing the game screen
                                                 """

    # drawing the window background
    win.blit(game_bg, (0, 0))

    # drawing the field background
    draw_field_background(win)

    # rendering the texts above the fields - ships, moves left and ships left
    render_texts(win, game, player)

    # drawing the field horizontal and vertical lines
    draw_field_lines(win)

    # drawing the squares
    draw_squares(win, squares, mouse_pos, player, game)


def draw_field_background(win):
    for idx in range(2):
        # field background
        pygame.draw.rect(win, GRAY, field_background_pos[idx])

        # background for the texts above the player fields
        pygame.draw.rect(win, BLACK, stats_text_background_pos[idx])


def render_texts(win, game, player):

    # updating the text values from the game variables
    texts[4].text = str(game.ships[player])
    texts[11].text = str(game.ships[player - 1])

    texts[5].text = str(game.moves_left[player])
    texts[12].text = str(game.moves_left[player - 1])

    texts[6].text = str(game.ships_killed[player])
    texts[13].text = str(game.ships_killed[player - 1])

    # rendering the texts
    for text in texts:
        text.render(win)


def draw_field_lines(win):
    """
        This function is drawing the horizontal and vertical lines of the field
                                                                                """

    # giving the initial positions and resetting every time the function is called
    points = [[26, 176, 465, 176], [726, 176, 1165, 176]]
    points2 = [[26, 176, 26, 616], [726, 176, 726, 616]]

    # creating 2 iterations for both player clients
    for p in range(2):

        # drawing the horizontal lines
        for horizontal_line in range(11):
            line = Line(
                start_x=points[p][0], start_y=points[p][1],
                end_x=points[p][2], end_y=points[p][3]
            )

            line.draw(win)

            # changing the positions for every line
            points[p][1] += 44
            points[p][3] += 44

        # doing the same here for the vertical lines
        for vertical_line in range(11):
            line = Line(
                start_x=points2[p][0], start_y=points2[p][1],
                end_x=points2[p][2], end_y=points2[p][3]
            )

            line.draw(win)

            points2[p][0] += 44
            points2[p][2] += 44


def draw_squares(win, squares, mouse_pos, player, game):
    """
        This function is drawing the player squares - they are being reversed in the game.py file so every client
    receives the correct squares.
                                  """

    my_squares, enemy_squares = squares

    # drawing the player squares as per usual
    for square in my_squares:
        square.draw(win)

    # drawing enemy squares if it is our turn
    if is_my_turn(player, game):
        for square in enemy_squares:
            # if the square is not dead and is hovered, it turns red and if we click, we can attack it
            if not square.is_dead():
                if square.is_hovered(mouse_pos):
                    square.color = RED
                else:
                    square.color = GRAY
            square.draw(win)

    # drawing enemy squares if it is not our turn - drawing as per usual
    else:
        for square in enemy_squares:
            square.draw(win)


def draw(win, screen, mouse_pos, game, player, squares, end_txt):
    """
        This is the main drawing function
                                            """

    win.fill(BLACK)

    if screen == "menu":
        draw_menu_screen(win, mouse_pos)

    elif screen == "waiting":
        waiting_text.render(win)

    elif screen == "game":
        draw_game_screen(win, player, squares, mouse_pos, game)

    else:
        end_txt.render(win)

        back_to_menu_btn.color = GRAY
        if back_to_menu_btn.is_hovered(mouse_pos):
            back_to_menu_btn.color = GREEN

        back_to_menu_btn.draw(win)

    pygame.display.update()


def main():
    """
        This is the main function running the game
                                                    """

    running = True
    clock = pygame.time.Clock()
    screen = "menu"

    network = Network()
    player = int(network.get_server_data())

    squares = [[], []]
    end_text = ''

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        # getting the game object on every iteration
        try:
            game = network.send("get")
        except Exception as e:
            print("[ERROR] ", e)
            break

        # if the players are connected but the screen is not the game yet, we get the squares
        if game.players_are_connected() and screen != "game":
            squares = game.get_squares(player)
            screen = "game"

        # if there was an action - someone attacked, we get update the squares for both players
        if game.squares_need_update[player]:

            try:
                squares = network.send("square_update")
            except Exception as e:
                print("[ERROR] ", e)

        # checking if someone's ships are 0, if they are the other player won, and we end the game
        if 0 in game.ships:
            screen = "won"
            player_won = game.ships.index(0)
            if player_won == player:
                end_text = end_texts[1]
            else:
                end_text = end_texts[0]

        # checking if someone's moves are 0, if they are the player with more ships won, otherwise it will be a tie
        elif 0 in game.moves_left:
            screen = "won"
            if game.ships[0] > game.ships[1]:
                player_won = 0
            elif game.ships[1] > game.ships[0]:
                player_won = 1
            else:
                player_won = -1

            if player_won == -1:
                end_text = end_texts[2]
            elif player_won == player:
                end_text = end_texts[1]
            else:
                end_text = end_texts[0]

        # here we are checking for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break

            # checking for events while in the menu screen - if the player hits new game, they are connected
            if screen == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menu_buttons:
                        if button.is_hovered(mouse_pos):
                            if button.text == "New Game":
                                screen = "waiting"

                                try:
                                    network.send("connect")
                                except Exception as e:
                                    print("[ERROR] ", e)

                            else:
                                running = False
                                break

            # checking for events in the game screen, if a player attacked or missed
            elif screen == "game":
                if is_my_turn(player, game):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        hit, idx = attack_enemy(squares)
                        if hit != "ignore":

                            try:
                                network.send(f"attack {hit} {idx}")
                            except Exception as e:
                                print("[ERROR] ", e)

            # checking for events when the game has ended - exit or back to main menu, player is disconnected
            elif screen == "won":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_to_menu_btn.is_hovered(mouse_pos):

                        try:
                            network.send("disconnect")
                        except Exception as e:
                            print("[ERROR] ", e)

                        screen = "menu"

        # calling the main draw function with all the needed parameters here
        draw(win, screen, mouse_pos, game, player, squares, end_text)
    pygame.quit()


if __name__ == '__main__':
    main()
