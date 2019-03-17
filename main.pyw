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

    speed = Text('average speed: ' + str(round(level_state.speed, 2)) + ' symbols per minute', width // 2,
                 height // 2 - 30, 36)
    mistakes = Text('mistakes: ' + str(level_state.mistakes) + ' (' + str(round(level_state.mistake_percentage(), 2))
                    + '%)', width // 2, height // 2 + 30, 36)
    btn_main = Button(80, 50, 'back', str(Path('images/button_inactive.png')), str(Path('images/button_active.png')),
                      arguments(screen)(main_menu), 120)
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
    gui = pygame.sprite.Group()
    gui.add(string)
    gui.add(speed)
    gui.add(mistakes)

    state.time_start()
    while True:
        speed.set_text('speed: ' + str(int(state.current_speed())) + ' symbols per minute')
        mistakes.set_text('mistakes: ' + str(state.mistakes) + ' (' + str(int(state.mistake_percentage())) + '%)')

        for event in pygame.event.get():
            gui.update(screen)
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
    lesson_paths = [str(path / f) for f in os.listdir(path) if f.endswith('.lesson')]
    lessons = []
    for lesson_path in lesson_paths:
        lesson_file = open(lesson_path, 'r')
        lesson_info = lesson_file.read().splitlines()
        lessons.append((lesson_info[0], arguments(screen, lesson_info[1], lesson_info[0])(main_loop)))
        lesson_file.close()

    caption = Text('choose lesson:', width // 2, height // 4, 50)
    selector = Selector(width // 2, height // 2, [x[0] for x in lessons], [x[1] for x in lessons])
    gui = pygame.sprite.Group()
    gui.add(selector)
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
            txt1 = Text('average speed: ' + stat[1][i][0] + ' symbols per minute', width // 2,
                        height // 4 - 25 + i * 120, 36)
            txt1.set_position(130, height // 4 - 40 + i * 85)
            txt2 = Text('mistakes: ' + stat[1][i][1] + '%', width // 2, height // 4 + 25 + i * 120, 36)
            txt2.set_position(130, height // 4 + i * 85)
            tmp_speed.append(txt1)
            tmp_mistakes.append(txt2)
        speed[stat[0]] = tmp_speed
        mistakes[stat[0]] = tmp_mistakes

    numbering = [Text(str(i+1) + '.', 100, height // 4 - 23 + i * 85, 36) for i in range(5)]
    btn_main = Button(80, 50, 'back', str(Path('images/button_inactive.png')), str(Path('images/button_active.png')),
                      arguments(screen)(main_menu), 120)
    selector = Selector(width // 2, 50, [x[0] for x in stats], [None] * len(stats))
    no_stats = Text('no statistics yet', width // 2, height // 2, 36)
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


def main_menu(screen):
    """Creates a main menu window.

    Args:
        screen: pygame screen to display content

    """
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    screen.fill(white)

    caption = Text('keyboard trainer', width // 2, height // 4, 80)
    btn_play = Button(width // 2, height // 2, 'play', str(Path('images/button_inactive.png')),
                      str(Path('images/button_active.png')), arguments(screen)(select_lesson), 300)
    btn_stats = Button(width // 2, height // 2 + 100, 'statistics', str(Path('images/button_inactive.png')),
                       str(Path('images/button_active.png')), arguments(screen)(stats), 300)
    btn_quit = Button(width // 2, height // 2 + 200, 'exit', str(Path('images/button_inactive.png')),
                      str(Path('images/button_active.png')), quit, 300)
    gui = pygame.sprite.Group()
    gui.add(btn_play)
    gui.add(btn_stats)
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
    screen = pygame.display.set_mode((1000, 600))
    main_menu(screen)
