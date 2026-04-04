import pygame, numpy as np, settings, random

# Importing from settings, the main file uses this
chip_size = settings.chip_size

# Initializing fonts
pygame.font.init()
comic_sans = pygame.font.SysFont('Comic Sans MS', chip_size//2)
sys_font = pygame.font.SysFont(None, int(chip_size * 0.8))


class Board:
    def __init__(self):
        # State #
        # 0-23 is the board from white house to black house
        # 24 is removed whites
        # 25 is removed blacks
        # 26 is white bear off
        # 27 is black bear off
        self.state = np.zeros(28, int)
        self.winner = 0

    def set(self):
        self.winner = 0
        self.state = np.zeros(28, int)
        self.state[0] = 2
        self.state[5] = -5
        self.state[7] = -3
        self.state[11] = 5
        self.state[12] = -5
        self.state[16] = 3
        self.state[18] = 5
        self.state[23] = -2

    def click(self):
        self.set()

    def get_valid_moves(self, dice):
        if self.winner != 0:
            return []
        state = self.state*dice.turn # Same color will be pos
        valid_moves = []

        # General case
        if (state[24:26] < 1).all():
            for d in set(dice.remaining):
                if dice.turn == 1: # White
                    for i in range(24-d):
                        if state[i] > 0 and state[i+d] >= -1:
                            valid_moves.append((i, i+d, d))
                else: # Black
                    for i in range(d, 24):
                        if state[i] > 0 and state[i-d] >= -1:
                            valid_moves.append((i, i-d, d))

        # if we have a piece removed
        else:
            for d in set(dice.remaining):
                if dice.turn == 1:
                    if state[24] > 0 and state[d-1] >= -1:
                        valid_moves.append((24, d-1, d))
                else:
                    if state[25] > 0 and state[24-d] >= -1:
                        valid_moves.append((25, 24-d, d))

        # Bear off for white
        if dice.turn == 1 and (state[:18]<1).all():
            for d in set(dice.remaining):
                if state[24-d] > 0:
                    valid_moves.append((24-d, 26, d))
                # Overshoot for white
                elif (state[18:24 - d] < 1).all():
                    for p in range(24 - d + 1, 24):
                        if state[p] > 0:
                            valid_moves.append((p, 26, d))
                            break
        # Bear off for black
        elif dice.turn == -1 and (state[6:24]<1).all():
            for d in set(dice.remaining):
                if state[d-1] > 0:
                    valid_moves.append((d-1, 27, d))
                # Overshoot for black
                elif (state[d:6] < 1).all():
                    for p in range(d - 2, -1, -1):
                        if state[p] > 0:
                            valid_moves.append((p, 27, d))
                            break
        return valid_moves


    def make_move(self, dice, move):
        # Checking for hits
        if self.state[move[0]] * self.state[move[1]] < 0:
            # Moving the removed piece in its new place
            self.state[move[1]] += dice.turn
            if dice.turn == 1:
                self.state[25] -= dice.turn
            else:
                self.state[24] -= dice.turn

        # Moving the piece
        self.state[move[0]] -= dice.turn
        self.state[move[1]] += dice.turn

        # Checking for win
        if self.state[26] == 15:
            self.winner = 1
        elif self.state[27] == -15:
            self.winner = -1

        # Removing the used dice
        dice.remaining.remove(move[2])

        # Returning board state
        return self.state

    def get_valid_turns(self, dice):
        # Returning nothing if the game is over

        all_paths_found = []
        # First we find all possible paths
        def search_paths(c_board, c_dice, c_path):
            # Closing down paths
            moves = c_board.get_valid_moves(c_dice)
            if not moves:
                current = tuple(c_board.state)
                all_paths_found.append((c_path, current))
                return

            # Discovering new paths
            for move in moves:
                # Copying the board
                ghost = Board()
                ghost.state = c_board.state.copy()

                # Copying the dice
                g_dice = Dice()
                g_dice.turn = c_dice.turn
                g_dice.remaining = list(c_dice.remaining)

                # Making the move on the board
                ghost.make_move(g_dice, move)

                # Recursive call
                search_paths(ghost, g_dice, c_path + [move])

        # Doing the search
        search_paths(self, dice, [])

        # Determining the longest move, cause we have to make a move just as long according to the rules
        max_path_length = max([len(path) for path, state in all_paths_found])
        unique_paths = []
        unique_states = set()

        # Returning nothing, if there are no legal moves
        if max_path_length == 0:
            return unique_paths, unique_states
        # Removing duplicates
        for path, state in all_paths_found:
            if len(path) == max_path_length and state not in unique_states:
                unique_states.add(state)
                unique_paths.append(path)
        return unique_paths, unique_states

    def draw_pieces(self, surface):
        state = self.state
        state, removed_whites, removed_blacks, white_bear_off, black_bear_off = state[:24].reshape((2, 12)), state[24], state[25], state[26], state[27]
        # First row
        x_offset = chip_size * 7
        for j in range(2):
            for i, x in enumerate(range(6 * chip_size, 0, -chip_size)):
                chip_count = abs(state[(0, i + j * 6)])
                if state[(0, i + j * 6)] > 0:
                    for k in range(chip_count):
                        center = (x + x_offset + chip_size / 2, chip_size * 3 + chip_size * k)
                        if k < 5:
                            pygame.draw.circle(surface, (255, 255, 255), center, chip_size / 2)
                            pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
                elif state[(0, i + j * 6)] < 0:
                    for k in range(chip_count):
                        center = (x + x_offset + chip_size / 2, chip_size * 3 + chip_size * k)
                        if k < 5:
                            pygame.draw.circle(surface, (135, 0, 0), center, chip_size / 2)
                            pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
                if chip_count > 5:
                    text_surface = comic_sans.render(f"+{chip_count - 5}", False, (0, 0, 0))
                    surface.blit(text_surface, (x + x_offset + chip_size / 10, chip_size * 2.6))
            x_offset = chip_size / -2

        # Second row
        x_offset = 0
        for j in range(2):
            for i, x in enumerate(range(chip_size // 2, 6 * chip_size, chip_size)):
                chip_count = abs(state[(1, i + j * 6)])
                if state[(1, i + j * 6)] > 0:
                    for k in range(chip_count):
                        center = (x + x_offset + chip_size / 2, chip_size * 13.5 - chip_size * k)
                        if k < 5:
                            pygame.draw.circle(surface, (255, 255, 255), center, chip_size / 2)
                            pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
                elif state[(1, i + j * 6)] < 0:
                    for k in range(chip_count):
                        center = (x + x_offset + chip_size / 2, chip_size * 13.5 - chip_size * k)
                        if k < 5:
                            pygame.draw.circle(surface, (135, 0, 0), center, chip_size / 2)
                            pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
                if chip_count > 5:
                    text_surface = comic_sans.render(f"+{chip_count - 5}", False, (0, 0, 0))
                    surface.blit(text_surface, (x + x_offset + chip_size / 10, chip_size * 13.1))
            x_offset = chip_size * 7.5

        # Removed pieces
        if removed_whites > 0:
            center = (settings.Width / 2, chip_size * 7.5)
            pygame.draw.circle(surface, (255, 255, 255), center, chip_size / 2)
            pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
            if removed_whites > 1:
                text_surface = comic_sans.render(f"+{removed_whites - 1}", False, (0, 0, 0))
                surface.blit(text_surface, text_surface.get_rect(center=center))
        if removed_blacks < 0:
            center = (settings.Width / 2, chip_size * 9)
            pygame.draw.circle(surface, (135, 0, 0), center, chip_size / 2)
            pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
            if removed_blacks < -1:
                text_surface = comic_sans.render(f"+{-removed_blacks - 1}", False, (0, 0, 0))
                surface.blit(text_surface, text_surface.get_rect(center=center))

        # Bear off
        for i in range(white_bear_off):
            rect = (chip_size * 6.75, chip_size * 9.75 + i * chip_size * 4 / 15, chip_size, chip_size * 4 / 15)
            pygame.draw.rect(surface, (255, 255, 255), rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        for i in range(-black_bear_off):
            rect = (chip_size * 6.75, chip_size * 2.75 + i * chip_size * 4 / 15, chip_size, chip_size * 4 / 15)
            pygame.draw.rect(surface, (135, 0, 0), rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 2)


class Dice:
    def __init__(self, x=0, y=0):
        # The turn color is 1 for white, -1 for black
        self.turn = -1
        self.x = x
        self.y = y
        self.remaining = []
        self.state = (6, 6)
        self.size = chip_size

    def roll(self):
        self.remaining = []
        self.state = (random.randint(1, 6), random.randint(1, 6))
        if self.state[0] == self.state[1]:
            [self.remaining.append(self.state[0]) for _ in range(4)]
        else:
            [self.remaining.append(i) for i in self.state]


    def click(self):
        self.roll() # Roll on click


    def __str__(self):
        # This is for printing
        return f"{self.state[0]}, {self.state[1]}"

    def draw(self, surface):

        # Color
        if self.turn == 1:
            dice_color = (255, 255, 255)
        else:
            dice_color = (135, 0, 0)
        border_color = (0, 0, 0)
        text_color = (0, 0, 0)

        spacing = self.size / 2

        # Cords
        rect1 = pygame.Rect(self.x, self.y, self.size, self.size)
        rect2 = pygame.Rect(self.x + self.size + spacing, self.y, self.size, self.size)

        # Draw dices
        pygame.draw.rect(surface, dice_color, rect1)
        pygame.draw.rect(surface, border_color, rect1, 2)

        pygame.draw.rect(surface, dice_color, rect2)
        pygame.draw.rect(surface, border_color, rect2, 2)

        # Text on dices
        text1_surface = sys_font.render(str(self.state[0]), True, text_color)
        text1_rect = text1_surface.get_rect(center=rect1.center)
        surface.blit(text1_surface, text1_rect)

        text2_surface = sys_font.render(str(self.state[1]), True, text_color)
        text2_rect = text2_surface.get_rect(center=rect2.center)
        surface.blit(text2_surface, text2_rect)


class Button:
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text
        self.color_normal = (200, 200, 200)
        self.color_click = (100, 100, 100)

    def draw(self, surface):
        # Check if mouse is currently held down over the button
        is_clicked = pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
        current_color = self.color_click if is_clicked else self.color_normal

        # Draw background
        pygame.draw.rect(surface, current_color, self.rect)

        # Render and center text
        text_surf = comic_sans.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event, dice_object):
        # Trigger the click event of the object
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                dice_object.click()


def draw_board(surface):
    y_offset = chip_size * 2.5
    pygame.draw.rect(surface, (245, 208, 135), [0, chip_size * 2, chip_size * 14.5, chip_size * 12.5])

    # First row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size // 2, 6 * chip_size, chip_size)):
            if i % 2 == 0:
                color = (255, 255, 255)
            else:
                color = (135, 0, 0)
            cords = [(x + x_offset, y_offset), (x + chip_size / 2 + x_offset, chip_size * 5 + y_offset),
                     (x + chip_size + x_offset, y_offset)]
            pygame.draw.polygon(surface, color, cords)
        x_offset = chip_size * 7.5

    # Second row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size // 2, 6 * chip_size, chip_size)):
            if i % 2 == 0:
                color = (135, 0, 0)
            else:
                color = (255, 255, 255)
            cords = [(x + x_offset, chip_size * 14), (x + chip_size / 2 + x_offset, chip_size * 6.5 + y_offset),
                     (x + chip_size + x_offset, chip_size * 14)]
            pygame.draw.polygon(surface, color, cords)
        x_offset = chip_size * 7.5

    # Holders
    pygame.draw.rect(surface, (0, 0, 0), [chip_size // 2, y_offset, chip_size * 13.5, chip_size * 11.5 + 1], 4)
    pygame.draw.rect(surface, (0, 0, 0), [chip_size * 6.5, y_offset, chip_size * 1.5, chip_size * 11.5], 2)
    pygame.draw.rect(surface, (0, 0, 0),[chip_size * 6.75, y_offset + chip_size * .25, chip_size * 1, chip_size * 4], 2)
    pygame.draw.rect(surface, (0, 0, 0),[chip_size * 6.75, y_offset + chip_size * 7.25, chip_size * 1, chip_size * 4], 2)


def clear(surface):
    surface.fill((50, 50, 50))
