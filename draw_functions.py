import pygame, settings, math

# Importing from settings, the main file also uses this
chip_size = settings.chip_size
Height = 14.5*chip_size
Width = 14.5*chip_size


pygame.font.init()
comic_sans = pygame.font.SysFont('Comic Sans MS', chip_size//2)
sys_font = pygame.font.SysFont(None, int(chip_size * 0.8))


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

def draw_pieces(surface, board):
    state = board.state
    removed_whites, removed_blacks, white_bear_off, black_bear_off = state[24], state[25], state[26], state[27]
    state = (state[:12], state[12:24])
    # First row
    x_offset = chip_size * 7
    for j in range(2):
        for i, x in enumerate(range(6 * chip_size, 0, -chip_size)):
            chip_count = abs(state[0][i + j * 6])
            if state[0][i + j * 6] > 0:
                for k in range(chip_count):
                    center = (x + x_offset + chip_size / 2, chip_size * 3 + chip_size * k)
                    if k < 5:
                        pygame.draw.circle(surface, (255, 255, 255), center, chip_size / 2)
                        pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
            elif state[0][i + j * 6] < 0:
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
            chip_count = abs(state[1][i + j * 6])
            if state[1][i + j * 6] > 0:
                for k in range(chip_count):
                    center = (x + x_offset + chip_size / 2, chip_size * 13.5 - chip_size * k)
                    if k < 5:
                        pygame.draw.circle(surface, (255, 255, 255), center, chip_size / 2)
                        pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
            elif state[1][i + j * 6] < 0:
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
        center = (Width / 2, chip_size * 7.5)
        pygame.draw.circle(surface, (255, 255, 255), center, chip_size / 2)
        pygame.draw.circle(surface, (0, 0, 0), center, chip_size / 2, 2)
        if removed_whites > 1:
            text_surface = comic_sans.render(f"+{removed_whites - 1}", False, (0, 0, 0))
            surface.blit(text_surface, text_surface.get_rect(center=center))
    if removed_blacks < 0:
        center = (Width / 2, chip_size * 9)
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


def draw_dice(surface, dice):

    # Color
    if dice.turn == 1:
        dice_color = (255, 255, 255)
    else:
        dice_color = (135, 0, 0)
    border_color = (0, 0, 0)
    text_color = (0, 0, 0)

    spacing = chip_size / 2

    # Cords
    rect1 = pygame.Rect(dice.x, dice.y, chip_size, chip_size)
    rect2 = pygame.Rect(dice.x + chip_size + spacing, dice.y, chip_size, chip_size)

    # Draw dices
    if dice.state[0] in dice.remaining:
        pygame.draw.rect(surface, dice_color, rect1)
        pygame.draw.rect(surface, border_color, rect1, 2)
    else:
        pygame.draw.rect(surface, (100, 100, 100), rect1)
        pygame.draw.rect(surface, border_color, rect1, 2)

    if dice.state[1] in dice.remaining:
        pygame.draw.rect(surface, dice_color, rect2)
        pygame.draw.rect(surface, border_color, rect2, 2)
    else:
        pygame.draw.rect(surface, (100, 100, 100), rect2)
        pygame.draw.rect(surface, border_color, rect2, 2)
    # Text on dices
    text1_surface = sys_font.render(str(dice.state[0]), True, text_color)
    text1_rect = text1_surface.get_rect(center=rect1.center)
    surface.blit(text1_surface, text1_rect)

    text2_surface = sys_font.render(str(dice.state[1]), True, text_color)
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

    def check(self, event):
        # Trigger the click event of the object
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def clear(surface):
    surface.fill((50, 50, 50))


def get_point_from_mouse(pos):
    x, y = pos
    y_offset = 2.5 * chip_size
    y_mid = (Height-y_offset) / 2 + y_offset

    # Check if clicking on removed pieces (Bar)
    if chip_size * 6.5 < x < chip_size * 8 and chip_size * 6.75 < y < chip_size * 9.75:
        if y > y_mid:
            return 25
        else:
            return 24

    # Check if clicking on Bear Off
    if chip_size * 6.5 < x < chip_size * 8:
        if y < y_mid:
            return 27
        else:
            return 26

    field = 0
    if y > y_offset:
        field += (Width / chip_size) - (x / chip_size) - .5
        if field > 7:
            field -= 1.5
        if not 0 < field < 12:
            return None
        if y > y_mid:
            field = 24-field
        if y > 14*chip_size:
            return None
        return math.floor(field)

    return None  # Clicked outside valid areas
