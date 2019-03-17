"""This module includes in-game entities, classes of GUI elements and constants"""
import pygame
import time


fps = 60
white = (255, 255, 255)
black = (0, 0, 0)


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

    def __init__(self, text, x, y, font_size, font_color=black, font_path='fonts\\freesansbold.ttf'):
        super().__init__()
        self.font = pygame.font.Font(font_path, font_size)
        self.font_color = font_color
        self.image = self.font.render(text, True, self.font_color)
        self.rect = self.image.get_rect()
        self.set_center_position(x, y)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, img_inactive, img_active, action=None, width=250, height=70):
        super().__init__()
        self.text = text
        self.img_active = pygame.image.load(img_active).convert()
        self.img_inactive = pygame.image.load(img_inactive).convert()
        self.action = action

        font = pygame.font.Font('fonts\\freesansbold.ttf', 50)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        self.text = (text_surface, text_rect)

        w = max(text_rect.width + 20, width)
        h = max(text_rect.height + 20, height)
        self.img_inactive = pygame.transform.scale(self.img_inactive, (w, h))
        self.img_active = pygame.transform.scale(self.img_active, (w, h))
        self.image = self.img_inactive

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.text[1].center = (self.rect.width // 2, self.rect.height // 2)

        self.img_inactive.blit(self.text[0], self.text[1])
        self.img_active.blit(self.text[0], self.text[1])

    def update(self, screen, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.rect.x < mouse_x < self.rect.x + self.rect.width
                and self.rect.y < mouse_y < self.rect.y + self.rect.height):
            self.image = self.img_active
            if event.type == pygame.MOUSEBUTTONDOWN and self.action is not None:
                if event.button == 1:
                    self.action()
        else:
            self.image = self.img_inactive


class Selector(pygame.sprite.Sprite):

    def prev(self):
        self.curr = (self.curr - 1) % len(self.lst)
        self.update_state = True

    def next(self):
        self.curr = (self.curr + 1) % len(self.lst)
        self.update_state = True

    def compound_buttons(self):
        if self.update_state:
            c_x, c_y = self.rect.center
            self.btn_center = Button(c_x, c_y, self.lst[self.curr], 'images\\selector_center_inactive.png',
                                     'images\\selector_center_active.png', self.actions[self.curr])
            self.btn_left = Button(c_x - (self.btn_center.rect.width + 70) // 2, c_y, '',
                                   'images\\selector_left_inactive.png', 'images\\selector_left_active.png', self.prev,
                                   70, 70)
            self.btn_right = Button(c_x + (self.btn_center.rect.width + 70) // 2, c_y, '',
                                    'images\\selector_right_inactive.png', 'images\\selector_right_active.png',
                                    self.next, 70, 70)

            self.image = pygame.Surface([self.btn_center.rect.width + 140, 70])
            self.rect = self.image.get_rect()
            self.rect.center = (c_x, c_y)

            self.group.empty()
            self.group.add(self.btn_center)
            self.group.add(self.btn_left)
            self.group.add(self.btn_right)
            self.update_state = False

        for btn in self.group:
            curr_rect = btn.rect.copy()
            curr_rect.center = (curr_rect.center[0] - self.rect.center[0] + self.rect.width // 2,
                                curr_rect.center[1] - self.rect.center[1] + self.rect.height // 2)
            self.image.blit(btn.image, curr_rect)

    def __init__(self, x, y, lst, actions):
        super().__init__()
        self.lst = lst if len(lst) > 0 else ['']
        self.actions = actions if len(actions) > 0 else [None]
        self.curr = 0
        self.update_state = False
        self.group = pygame.sprite.Group()

        self.btn_center = Button(x, y, self.lst[0], 'images\\selector_center_inactive.png',
                                 'images\\selector_center_active.png',
                                 self.actions[0])
        self.btn_left = Button(x - (self.btn_center.rect.width + 70) // 2, y, '', 'images\\selector_left_inactive.png',
                               'images\\selector_left_active.png', self.prev, 70, 70)
        self.btn_right = Button(x + (self.btn_center.rect.width + 70) // 2, y, '',
                                'images\\selector_right_inactive.png', 'images\\selector_right_active.png', self.next,
                                70, 70)

        self.image = pygame.Surface([self.btn_center.rect.width + 140, 70])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.group.add(self.btn_left)
        self.group.add(self.btn_center)
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
        if not self.complete and event.unicode == self.lesson[self.curr_letter]:
            self.next_letter()
        elif event.unicode != '':
            self.mistakes += 1


class LevelString(pygame.sprite.Sprite):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()

    def update(self, screen):
        font = pygame.font.Font('fonts\\freesansbold.ttf', 72)
        text_surface = font.render(self.state.lesson[self.state.curr_letter:self.state.curr_letter + 25], True,
                                   black, (240, 240, 240))
        self.image = text_surface
        self.rect = text_surface.get_rect()
        self.rect.x = screen.get_rect().width // 2
        self.rect.y = (screen.get_rect().height - self.rect.height) // 2
