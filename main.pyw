import pygame
from entities import *
from utilfuncs import *
import os


def level_finished(screen, level_state):
    """Displays statistics after successfully finished lesson.

    Args:
        screen: pygame screen to display content
        level_state: an object that keeps lesson statistics

    """
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    screen.fill(white)

    stats = read_stats()
    curr_speed = str(round(level_state.speed, 2))
    curr_mistakes = str(round(level_state.mistake_percentage(), 2))
    for stat in stats:
        if stat[0] == level_state.lesson_name:
            for i in range(len(stat[1])):
                if stat[1][i][0] == '-':
                    stat[1][i] = (curr_speed, curr_mistakes)
                    break
            else:
                stat[1].insert(0, (curr_speed, curr_mistakes))
                stat[1].pop()
            break
    else:
        temp_results = [(curr_speed, curr_mistakes)]
        for i in range(4):
            temp_results.append(('-', '-'))
        stats.append((level_state.lesson_name, temp_results))

    stats_file = open('stats.log', 'w')
    for stat in stats:
        output = stat[0] + '@' + ' '.join(all_elements(stat[1])) + '\n'
        stats_file.write(output)
    stats_file.close()

    speed = Text('average speed: ' + str(round(level_state.speed, 2)) +
                 ' symbols per minute', width // 2, height // 2 - 30, 36)
    mistakes = Text('mistakes: ' + str(level_state.mistakes) + ' (' +
                    str(round(level_state.mistake_percentage(), 2)) + '%)',
                    width // 2, height // 2 + 30, 36)
    btn_main = SimpleButton(120, 55, 200, 70, 'back',
                            arguments(screen)(main_menu))
    gui = pygame.sprite.Group()
    gui.add(btn_main)
    gui.add(speed)
    gui.add(mistakes)

    while True:
        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.QUIT:
                quit()

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


def main_loop(screen, lesson, lesson_name):
    """Runs chosen lesson.

    Args:
        screen: pygame screen to display content
        lesson: a string that should be typed by player
        lesson_name: name of the chosen lesson

    """
    clock = pygame.time.Clock()
    state = LevelState(lesson, lesson_name)

    screen.fill(white)
    string = LevelString(state)
    speed = Text('speed:', 0, 0, 24)
    speed.set_position(10, 10)
    mistakes = Text('mistakes:', 0, 0, 24)
    mistakes.set_position(10, 40)
    btn_main = SimpleButton(screen.get_size()[1]*2 - 320, 55, 200, 70, 'back',
                            arguments(screen)(main_menu))
    gui = pygame.sprite.Group()
    gui.add(string)
    gui.add(speed)
    gui.add(mistakes)
    gui.add(btn_main)

    state.time_start()
    while True:
        speed.set_text('speed: ' + str(int(state.current_speed())) +
                       ' symbols per minute')
        mistakes.set_text('mistakes: ' + str(state.mistakes) + ' (' +
                          str(int(state.mistake_percentage())) + '%)')

        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.KEYDOWN:
                state.update(event)
            if event.type == pygame.QUIT:
                quit()
        if state.complete:
            level_finished(screen, state)

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


def select_lesson(screen):
    """Creates a window to select lesson.

    Args:
        screen: pygame screen to display content

    """
    clock = pygame.time.Clock()
    width, height = screen.get_size()
    screen.fill(white)

    path = Path('./lessons')
    lesson_paths = [str(path / f) for f in os.listdir(str(path)) if
                    f.endswith('.lesson')]
    lessons = []
    for lesson_path in lesson_paths:
        lesson_file = open(lesson_path, 'r')
        lesson_info = lesson_file.read().splitlines()
        lessons.append((lesson_info[0], arguments(screen, lesson_info[1],
                                                  lesson_info[0])(main_loop)))
        lesson_file.close()

    caption = Text('choose lesson:', width // 2, height // 3, 50)
    selector = SimpleSelector(width // 2, height // 2, [x[0] for x in lessons],
                              [x[1] for x in lessons])
    btn_main = SimpleButton(120, 55, 200, 70, 'back',
                            arguments(screen)(main_menu))
    gui = pygame.sprite.Group()
    gui.add(selector)
    gui.add(caption)
    gui.add(btn_main)

    while True:
        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.QUIT:
                quit()

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


def stats(screen):
    """Creates a window that contains statistics of the player.

    Args:
        screen: pygame screen to display content

    """
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    screen.fill(white)
    stats = read_stats()

    speed = {}
    mistakes = {}
    for stat in stats:
        tmp_speed = []
        tmp_mistakes = []
        for i in range(5):
            if stat[1][i][0] == '-':
                break
            txt1 = Text('average speed: ' + stat[1][i][0] +
                        ' symbols per minute', width // 2,
                        height // 4 - 25 + i * 120, 36)
            txt1.set_position(130, height // 4 - 40 + i * 85)
            txt2 = Text('mistakes: ' + stat[1][i][1] + '%', width // 2,
                        height // 4 + 25 + i * 120, 36)
            txt2.set_position(130, height // 4 + i * 85)
            tmp_speed.append(txt1)
            tmp_mistakes.append(txt2)
        speed[stat[0]] = tmp_speed
        mistakes[stat[0]] = tmp_mistakes

    numbering = [Text(str(i+1) + '.', 100, height // 4 - 23 + i * 85, 36)
                 for i in range(5)]
    selector = SimpleSelector(width // 2, 55, [x[0] for x in stats],
                              [None] * len(stats))
    btn_main = SimpleButton(120, 55, 200, 70, 'back',
                            arguments(screen)(main_menu))
    no_stats = Text('no statistics yet', width // 2, height // 2, 48)
    gui = pygame.sprite.Group()
    gui.add(btn_main)
    gui.add(selector)

    while True:

        curr = selector.get_current_choice()
        gui.empty()
        gui.add(btn_main)
        try:
            for i in range(len(speed[curr])):
                gui.add(speed[curr][i])
                gui.add(mistakes[curr][i])
                gui.add(numbering[i])
            gui.add(selector)
        except KeyError:
            gui.add(no_stats)

        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.QUIT:
                quit()

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


def lesson_saver(screen, text):
    """Creates a window for typing lesson name.

    Args:
        screen: pygame screen to display content
        text: content of lesson

    """
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    input_box = InputBox()
    saved = [False]
    caption = Text('type name of the lesson:', width // 2, height // 2.8, 48)
    btn_main = SimpleButton(120, 55, 200, 70, 'back',
                            arguments(screen)(main_menu))
    btn_save = SimpleButton(120, 155, 200, 70, 'save',
                            arguments(input_box.text, text,
                                      saved)(save_lesson))
    gui = pygame.sprite.Group()
    gui.add(input_box)
    gui.add(caption)
    gui.add(btn_main)
    gui.add(btn_save)

    while True:
        if saved[0]:
            main_menu(screen)

        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.QUIT:
                quit()

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


def lesson_creator(screen):
    """Creates a window to add custom lessons.

    Args:
        screen: pygame screen to display content

    """
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    text = ""
    input_box = InputBox()
    caption = Text('type your lesson:', width // 2, height // 2.8, 48)
    btn_main = SimpleButton(120, 55, 200, 70, 'back',
                            arguments(screen)(main_menu))
    btn_save = SimpleButton(120, 155, 200, 70, 'save',
                            arguments(screen, input_box.text)(lesson_saver))
    gui = pygame.sprite.Group()
    gui.add(input_box)
    gui.add(caption)
    gui.add(btn_main)
    gui.add(btn_save)

    while True:
        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.QUIT:
                quit()

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


def main_menu(screen):
    """Creates a main menu window.

    Args:
        screen: pygame screen to display content

    """
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    screen.fill(white)

    caption = Text('keyboard trainer', width // 2, height // 3.5, 100)
    btn_play = SimpleButton(width // 2, height // 2, 350, 70, 'play',
                            arguments(screen)(select_lesson))
    btn_stats = SimpleButton(width // 2, height // 2 + 100, 350, 70,
                             'statistics', arguments(screen)(stats))
    btn_editor = SimpleButton(width // 2, height // 2 + 200, 350, 70, 'editor',
                              arguments(screen)(lesson_creator))
    btn_quit = SimpleButton(width // 2, height // 2 + 300, 350, 70, 'exit',
                            quit)
    gui = pygame.sprite.Group()
    gui.add(btn_play)
    gui.add(btn_stats)
    gui.add(btn_editor)
    gui.add(btn_quit)
    gui.add(caption)

    while True:
        for event in pygame.event.get():
            gui.update(screen, event)
            if event.type == pygame.QUIT:
                quit()

        gui.draw(screen)
        pygame.display.update()
        screen.fill(white)
        clock.tick(fps)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("keyboard trainer")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    main_menu(screen)
