"""This module includes in-game entities, classes of GUI elements
and constants"""
import pygame
import pygame.locals as pl
import pygame.gfxdraw as gfx
import time
from pathlib import Path


fps = 60
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)


class Text(pygame.sprite.Sprite):
    def set_center_position(self, x, y):
        self.rect.center = (x, y)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_text(self, text):
        x, y = self.rect.x, self.rect.y
        self.image = self.font.render(text, True, self.font_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __init__(self, text, x, y, font_size, font_color=black,
                 font_path=str(Path('fonts/freesansbold.ttf'))):
        super().__init__()
        self.font = pygame.font.Font(font_path, font_size)
        self.font_color = font_color
        self.image = self.font.render(text, True, self.font_color)
        self.rect = self.image.get_rect()
        self.set_center_position(x, y)


class SimpleButton(pygame.sprite.Sprite):
    def fill_with_outline(self, fill_color, outline_color, border=10):
        self.image.fill(outline_color)
        self.image.fill(fill_color,
                        self.image.get_rect().inflate(-border, -border))

    def set_image(self, active):
        self.text_surface = self.font.render(self.caption, True, black if not
                                             active else gray)
        self.text = (self.text_surface, self.text_rect)
        self.image = pygame.Surface([self.w, self.h])
        self.fill_with_outline(white, black if not active else gray)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.text[1].center = (self.rect.width // 2, self.rect.height // 2)
        if self.type == 'right_arrow':
            gfx.aapolygon(self.image, [[3 * self.w // 4, self.h // 2],
                          [self.w // 4, self.h // 4],
                          [self.w // 4, 3 * self.h // 4]], gray if active else
                          black)
            gfx.filled_polygon(self.image, [[3 * self.w // 4, self.h // 2],
                               [self.w // 4, self.h // 4],
                               [self.w // 4, 3 * self.h // 4]], gray if active
                               else black)
        elif self.type == 'left_arrow':
            gfx.aapolygon(self.image, [[self.w // 4, self.h // 2],
                          [3 * self.w // 4, self.h // 4],
                          [3 * self.w // 4, 3 * self.h // 4]], gray if active
                          else black)
            gfx.filled_polygon(self.image, [[self.w // 4, self.h // 2],
                               [3 * self.w // 4, self.h // 4],
                               [3 * self.w // 4, 3 * self.h // 4]], gray if
                               active else black)
        else:
            self.image.blit(self.text[0], self.text[1])

    def __init__(self, x, y, width, height, text, action=None, type=None):
        super().__init__()
        self.action = action
        self.type = type
        self.caption = text
        self.font = pygame.font.Font(str(Path('fonts/freesansbold.ttf')), 50)
        self.text_surface = self.font.render(self.caption, True, black)
        self.text_rect = self.text_surface.get_rect()
        self.text = (self.text_surface, self.text_rect)
        self.x = x
        self.y = y
        self.w = max(self.text_rect.width + 20, width)
        self.h = max(self.text_rect.height + 20, height)
        self.set_image(False)

    def update(self, screen, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.rect.x < mouse_x < self.rect.x + self.rect.width
                and self.rect.y < mouse_y < self.rect.y + self.rect.height):
            self.set_image(True)
            if (event.type == pygame.MOUSEBUTTONDOWN and
                    self.action is not None):
                if event.button == 1:
                    self.action()
        else:
            self.set_image(False)


class SimpleSelector(pygame.sprite.Sprite):

    def prev(self):
        self.curr = (self.curr - 1) % len(self.lst)
        self.update_state = True

    def next(self):
        self.curr = (self.curr + 1) % len(self.lst)
        self.update_state = True

    def compound_buttons(self):
        if self.update_state:
            c_x, c_y = self.rect.center
            self.btn_center = SimpleButton(c_x, c_y, 350, 70,
                                           self.lst[self.curr],
                                           self.actions[self.curr])
            self.btn_left = SimpleButton(c_x - (self.btn_center.rect.width +
                                         60) // 2, c_y, 70, 70, '', self.prev,
                                         'left_arrow')
            self.btn_right = SimpleButton(c_x + (self.btn_center.rect.width +
                                          60) // 2, c_y, 70, 70, '', self.next,
                                          'right_arrow')

            self.image = pygame.Surface([self.btn_center.rect.width + 130, 70])
            self.rect = self.image.get_rect()
            self.rect.center = (c_x, c_y)

            self.group.empty()
            self.group.add(self.btn_center)
            self.group.add(self.btn_left)
            self.group.add(self.btn_right)
            self.update_state = False

        for btn in self.group:
            curr_rect = btn.rect.copy()
            curr_rect.center = (curr_rect.center[0] - self.rect.center[0] +
                                self.rect.width // 2,
                                curr_rect.center[1] - self.rect.center[1] +
                                self.rect.height // 2)
            self.image.blit(btn.image, curr_rect)

    def __init__(self, x, y, lst, actions):
        super().__init__()
        self.lst = lst if len(lst) > 0 else ['']
        self.actions = actions if len(actions) > 0 else [None]
        self.curr = 0
        self.update_state = False
        self.group = pygame.sprite.Group()

        self.btn_center = SimpleButton(x, y, 350, 70, self.lst[0],
                                       self.actions[0])
        self.btn_left = SimpleButton(x - (self.btn_center.rect.width + 60)
                                     // 2, y, 70, 70, '', self.prev,
                                     'left_arrow')
        self.btn_right = SimpleButton(x + (self.btn_center.rect.width + 60)
                                      // 2, y, 70, 70, '', self.next,
                                      'right_arrow')

        self.image = pygame.Surface([self.btn_center.rect.width + 130, 70])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.group.add(self.btn_center)
        self.group.add(self.btn_left)
        self.group.add(self.btn_right)
        self.compound_buttons()

    def update(self, screen, event):
        self.compound_buttons()
        self.group.update(screen, event)

    def get_current_choice(self):
        return self.lst[self.curr]


class LevelState:
    def __init__(self, lesson, name):
        self.lesson_name = name
        self.lesson = lesson
        self.curr_letter = 0
        self.start_time = 0.0
        self.speed = 0.0
        self.mistakes = 0
        self.complete = False

    def time_start(self):
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time() - self.start_time

    def current_speed(self):
        return 60 * self.curr_letter / max(self.elapsed_time(), 1)

    def mistake_percentage(self):
        return 100 * self.mistakes / len(self.lesson)

    def next_letter(self):
        self.curr_letter += 1
        if self.curr_letter == len(self.lesson):
            self.complete = True
            self.speed = self.current_speed()

    def update(self, event):
        if (not self.complete and
                event.unicode == self.lesson[self.curr_letter]):
            self.next_letter()
        elif event.unicode != '':
            self.mistakes += 1


class LevelString(pygame.sprite.Sprite):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()

    def update(self, screen, *args):
        font = pygame.font.Font(str(Path('fonts/freesansbold.ttf')), 72)
        txt = self.state.lesson[self.state.curr_letter:
                                self.state.curr_letter + 25]
        text_surface = font.render(txt, True, black, (240, 240, 240))
        self.image = text_surface
        self.rect = text_surface.get_rect()
        self.rect.x = screen.get_rect().width // 3
        self.rect.y = (screen.get_rect().height - self.rect.height) // 2


class InputBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.text = [""]

    def update(self, screen, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pl.K_BACKSPACE:
                self.text[0] = self.text[0][:-1]
            else:
                self.text[0] += event.unicode
        font = pygame.font.Font(str(Path('fonts/freesansbold.ttf')), 72)
        text_surface = font.render(self.text[0], True, black, (240, 240, 240))
        self.image = text_surface
        self.rect = text_surface.get_rect()
        self.rect.topright = (2 * screen.get_rect().width // 3,
                              (screen.get_rect().height -
                              self.rect.height) // 2)
