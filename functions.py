import pygame, random, numpy as np, settings
from poetry.console.commands import self

# Importing from settings, the main file uses this
chip_size = settings.chip_size

# Initializing fonts
pygame.font.init()
comic_sans = pygame.font.SysFont('Comic Sans MS', chip_size//2)


class Board:
    def __init__(self, surface):
        self.state = np.zeros(24, int)
        self.surface = surface

    def set(self):
        self.state = np.zeros(24, int)
        self.state[0] = 5
        self.state[4] = -3
        self.state[6] = -5
        self.state[11] = 2
        self.state[12:] = -self.state[:12]

    def click(self):
        self.set()


class Dice:
    def __init__(self, x=0, y=0, size=50):
        self.x = x
        self.y = y
        self.state = (6, 6)
        self.size = size
        self.font = pygame.font.SysFont(None, int(self.size * 0.8))

    def click(self):
        # Roll on click
        self.state = (random.randint(1, 6), random.randint(1, 6))
        return self.state

    def __str__(self):
        # This is for printing
        return f"{self.state[0]}, {self.state[1]}"

    def draw(self, surface):

        # Color
        dice_color = (255, 255, 255)
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
        text1_surface = self.font.render(str(self.state[0]), True, text_color)
        text1_rect = text1_surface.get_rect(center=rect1.center)
        surface.blit(text1_surface, text1_rect)

        text2_surface = self.font.render(str(self.state[1]), True, text_color)
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

        # Render and center text (using your existing comic_sans font)
        text_surf = comic_sans.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event, dice_object):
        # Trigger the roll on the exact frame the mouse is clicked
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
    
def draw_pieces(surface, state):
    state = state.reshape((2, 12))
    # First row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size // 2, 6 * chip_size, chip_size)):
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
        x_offset = chip_size * 7.5

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

def clear(surface):
    surface.fill((50, 50, 50))
