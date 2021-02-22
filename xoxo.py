import pygame
from enum import Enum
import math

# GLOBAL VARS
S_WIDTH = 800
S_HEIGHT = 600

P_WIDTH = 500
P_HEIGHT = 500

P_X = (S_WIDTH - P_WIDTH) / 2
P_Y = (S_HEIGHT - P_HEIGHT) / 2

P_PADDING = 20

ROWS = 3
CELL_SIZE = (P_WIDTH - P_PADDING*2) // ROWS

BG_COLOR = (180, 180, 180)
PLAYGROUND_COLOR = (50, 50, 50)
DROPSHADOW_COLOR = (22, 22, 22)
GRID_COLOR = (200, 200, 200)
PLAYER_COLOR = (255, 255, 255)


class Pieces(Enum):
    NONE = 0
    X = 1
    O = 2


class Piece:
    def __init__(self, pieces):
        self.__piece = pieces

    def draw(self, surface, x, y, c_width, color, padding=10):
        if self.__piece == Pieces.X:
            print("X")

        if self.__piece == Pieces.O:
            pygame.draw.circle(surface, color, (x + (c_width - padding*2) / 2, y + (c_width - padding*2) / 2), c_width - (padding*2), 4)


class Board:

    def __init__(self, surface, playground_x, playground_y, playground_width, playground_height, row_count,
                 padding, grid_color, bg_color, drop_shadow_color, playground_color, player_color):
        self.surface = surface
        self.__sw = surface.get_size()[0]
        self.__sh = surface.get_size()[1]
        self.__pw = playground_width
        self.__ph = playground_height
        self.__px = playground_x
        self.__py = playground_y
        self.__rows = row_count
        self.__padding = padding
        self.__cell_size = (self.__pw - self.__padding*2) / self.__rows
        self.__grid_color = grid_color
        self.__bg_color = bg_color
        self.__drop_shadow_color = drop_shadow_color
        self.__playground_color = playground_color
        self.__player_color = player_color

        self.__piece_list = [[Pieces.NONE for _ in range(self.__rows)] for _ in range(self.__rows)]
        self.__turn = 0
        self.__move_count = 0


    def set_piece_list(self, pl):
        self.__piece_list = pl

    def draw_playground(self):
        self.surface.fill(self.__bg_color)
        # drop shadow
        pygame.draw.rect(self.surface, self.__drop_shadow_color,
                         (self.__sw // 2 - self.__pw // 2 + self.__padding,
                          self.__sh // 2 - self.__ph // 2 + self.__padding,
                          self.__pw,
                          self.__ph),
                         0)
        # fill
        pygame.draw.rect(self.surface, self.__playground_color,
                         (self.__sw // 2 - self.__pw // 2,
                          self.__sh // 2 - self.__ph // 2,
                          self.__pw,
                          self.__ph),
                         0)
        # border
        pygame.draw.rect(self.surface, self.__grid_color,
                         (self.__sw // 2 - self.__pw // 2,
                          self.__sh // 2 - self.__ph // 2,
                          self.__pw,
                          self.__ph),
                         4)

    def draw_grid(self):
        for i in range(self.__rows - 1):
            # vertical lines
            pygame.draw.line(self.surface, self.__grid_color,
                             (self.__cell_size * i + self.__px + self.__padding + self.__cell_size,
                              self.__py + self.__padding),
                             (self.__cell_size * i + self.__px + self.__padding + self.__cell_size,
                              self.__py + self.__ph - self.__padding), 4)
            # horizontal lines
            pygame.draw.line(self.surface, self.__grid_color,
                             (self.__px + self.__padding,
                              self.__py + self.__cell_size * i + self.__cell_size + self.__padding),
                             (self.__px + self.__pw - self.__padding,
                              self.__py + self.__cell_size * i + self.__cell_size + self.__padding), 4)

    def draw_pieces(self):

        for c in range(len(self.__piece_list)):
            for r in range(len(self.__piece_list[c])):
                piece_x = c * self.__cell_size
                piece_y = r * self.__cell_size
                if self.__piece_list[c][r] == Pieces.X:
                    pygame.draw.line(self.surface, self.__player_color,
                                     (self.__px + self.__padding*2 + piece_x,
                                      self.__py + self.__padding*2 + piece_y),
                                     (self.__px + self.__cell_size + piece_x,
                                      self.__py + self.__cell_size + piece_y),
                                     10)
                    pygame.draw.line(self.surface, self.__player_color,
                                     (self.__px + self.__padding * 2 + piece_x,
                                      self.__py + self.__cell_size + piece_y),
                                     (self.__px + self.__cell_size + piece_x,
                                      self.__py + self.__padding*2 + piece_y),
                                     13)

                if self.__piece_list[c][r] == Pieces.O:
                    pygame.draw.circle(self.surface, self.__player_color,
                                       (self.__px + (self.__cell_size/2) + self.__padding + piece_x,
                                        self.__py + (self.__cell_size/2) + self.__padding + piece_y),
                                       (self.__cell_size/2) - self.__padding, 10)

    def input_manager(self, x, y ):
        current_piece = Pieces.X if self.__turn == 0 else Pieces.O
        if x > P_X + self.__padding and \
                x < P_X - self.__padding + self.__pw and \
                x > P_Y + self.__padding and \
                y < P_Y - self.__padding + self.__ph:
            list_x = x - ((self.__sw - self.__pw) / 2) - self.__padding
            list_x = math.floor(self.__rows / (self.__pw - self.__padding * 2) * list_x)
            list_y = y - ((self.__sh - self.__ph) / 2) - self.__padding
            list_y = math.floor(self.__rows / (self.__ph - self.__padding * 2) * list_y)

            if self.__piece_list[list_x][list_y] == Pieces.NONE:
                self.__piece_list[list_x][list_y] = current_piece

                self.__turn += 1
                self.__turn = self.__turn % 2
                self.__move_count += 1

                for i in range(self.__rows):
                    if self.__piece_list[list_x][i] != current_piece:
                        break
                    if i == self.__rows - 1:
                        return current_piece

                for i in range(self.__rows):
                    if self.__piece_list[i][list_y] != current_piece:
                        break
                    if i == self.__rows - 1:
                        return current_piece

                if list_x == list_y:
                    for i in range(self.__rows):
                        if self.__piece_list[i][i] != current_piece:
                            break
                        if i == self.__rows - 1:
                            return current_piece

                if list_x + list_y == self.__rows-1:
                    for i in range(self.__rows):
                        if self.__piece_list[i][(self.__rows-1) - i] != current_piece:
                            break
                        if i == self.__rows - 1:
                            return current_piece

                if self.__move_count == math.pow(self.__rows, 2):
                    print("draw")
                    return False

        return True


    def render(self):
        self.draw_playground()
        self.draw_pieces()
        self.draw_grid()
        pygame.display.update()

    def show_winner(self, piece):
        pygame.draw.rect(self.surface, self.__bg_color, (0, 0, self.__sw, self.__sh))

        font = pygame.font.SysFont("Helvetica", 100)
        title = font.render(f"{piece.name} wins!", 1, PLAYGROUND_COLOR)
        self.surface.blit(title, (self.__sw / 2 - title.get_width() / 2, (self.__sh / 2) - title.get_height() / 2))

        pygame.display.update()
        pygame.time.wait(1500)

    def show_draw(self):
        pygame.draw.rect(self.surface, self.__bg_color, (0, 0, self.__sw, self.__sh))

        font = pygame.font.SysFont("Helvetica", 100)
        title = font.render(f"DRAW!", 1, PLAYGROUND_COLOR)
        self.surface.blit(title, (self.__sw / 2 - title.get_width() / 2, (self.__sh / 2) - title.get_height() / 2))

        pygame.display.update()
        pygame.time.wait(1500)

    def update(self, x, y):
        status = self.input_manager(x, y)
        self.render()

        return status



def game(surface):
    is_running = True

    board = Board(surface, P_X, P_Y, P_WIDTH, P_HEIGHT, ROWS, P_PADDING, GRID_COLOR, BG_COLOR, DROPSHADOW_COLOR, PLAYGROUND_COLOR, PLAYER_COLOR)

    pygame.init()
    board.render()
    pygame.display.update()


    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                status = board.update(event.pos[0], event.pos[1])

                if status == Pieces.X or status == Pieces.O:
                    board.show_winner(status)
                    is_running = False
                elif not status:
                    board.show_draw()
                    is_running = False


def main():
    surface = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption("XOXO - v.0.1")
    surface.fill(BG_COLOR)

    pygame.font.init()
    game_is_running = True

    while game_is_running:
        surface.fill(BG_COLOR)

        font = pygame.font.SysFont("Helvetica", 100)
        title = font.render("XOXO", 1, PLAYGROUND_COLOR)
        surface.blit(title, (S_WIDTH / 2 - title.get_width() / 2, (S_HEIGHT / 2) - title.get_height() / 2))

        font = pygame.font.SysFont("Helvetica", 30)
        subline = font.render("press any key", 1, PLAYGROUND_COLOR)
        surface.blit(subline, (S_WIDTH / 2 - subline.get_width() / 2, (S_HEIGHT / 2) - subline.get_height() / 2 + title.get_height()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game(surface)


    pygame.quit()


if __name__ == "__main__":
    main()
