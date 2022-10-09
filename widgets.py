import pygame


class Button:
    def __init__(
            self, text='', font='comicsans', font_size=25,
            text_color=(0, 0, 0), x=0, y=0, width=0, height=0,
            color=(255, 255, 255)
    ):

        self.text = text
        self.font = font
        self.font_size = font_size
        self.text_color = text_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, True, self.text_color)
        win.blit(
            text,
            (
                self.x + round(self.width / 2) - round(text.get_width() / 2),
                self.y + round(self.height / 2) - round(text.get_height() / 2)
            )
        )

    def is_hovered(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if (self.x <= x1 <= self.x + self.width) and (self.y <= y1 <= self.y + self.height):
            return True
        return False


class Text:
    def __init__(self, text='', size=25, style='comicsans', color=(255, 255, 255), x=0, y=0):
        self.text = text
        self.size = size
        self.style = style
        self.color = color
        self.x = x
        self.y = y

    def render(self, win):
        font = pygame.font.SysFont(self.style, self.size)
        text = font.render(self.text, True, self.color)
        win.blit(text, (self.x, self.y))


class Line:
    def __init__(self, color=(0, 0, 0), start_x=0, start_y=0, end_x=0, end_y=0, width=1):
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.width = width

    def draw(self, win):
        pygame.draw.line(win, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y), self.width)


class Square:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.is_ship_ = False
        self.is_dead_ = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def is_hovered(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if (self.x <= x1 <= self.x + self.width) and (self.y <= y1 <= self.y + self.height):
            return True
        return False

    def is_ship(self):
        return self.is_ship_

    def is_dead(self):
        return self.is_dead_
