import curses
import time
import random

def init_colors():
    # Inicializace barevných párů a vrácení atributů pro hada, jablíčka a překážky
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    return curses.color_pair(1), curses.color_pair(2), curses.color_pair(3)

def init_obstacles(sw, sh, count=10):
    obstacles = []
    for _ in range(count):
        ox = random.randint(1, sw - 2)
        oy = random.randint(1, sh - 2)
        obstacles.append((oy, ox))
    return obstacles

def init_apples(sw, sh, obstacles, snake, count=3):
    apples = []
    for _ in range(count):
        ax = random.randint(1, sw - 2)
        ay = random.randint(1, sh - 2)
        while (ay, ax) in obstacles or (ay, ax) in snake or (ay, ax) in apples:
            ax = random.randint(1, sw - 2)
            ay = random.randint(1, sh - 2)
        apples.append((ay, ax))
    return apples

def draw_score(stdscr, score, sh, sw):
    score_str = f"Score: {score}"
    stdscr.addstr(sh - 1, sw - len(score_str) - 1, score_str, curses.A_BOLD)

def draw_obstacles(stdscr, obstacles, color):
    for (oy, ox) in obstacles:
        stdscr.addstr(oy, ox, "#", color)

def draw_apples(stdscr, apples, color):
    for (ay, ax) in apples:
        stdscr.addstr(ay, ax, "@", color)

def draw_snake(stdscr, snake, color):
    for idx, (sy, sx) in enumerate(snake):
        if idx == len(snake) - 1:
            stdscr.addstr(sy, sx, "O", color)
        else:
            stdscr.addstr(sy, sx, "o", color)

def check_collision(new_head, snake, obstacles, sh, sw):
    # Kontrola kolize s překážkou
    if new_head in obstacles:
        return "Chyba! Narazil jsi do překážky!"
    # Kontrola kolize se zdí
    head_y, head_x = new_head
    if head_x < 0 or head_x >= sw or head_y < 0 or head_y >= sh:
        return "Chyba! Narazil jsi do zdi!"
    # Kontrola kolize se sebou samým
    if new_head in snake:
        return "Chyba! Narazil jsi do sebe!"
    return ""

def generate_new_apple(sw, sh, obstacles, snake, apples):
    ax = random.randint(1, sw - 2)
    ay = random.randint(1, sh - 2)
    while (ay, ax) in obstacles or (ay, ax) in snake or (ay, ax) in apples:
        ax = random.randint(1, sw - 2)
        ay = random.randint(1, sh - 2)
    apples.append((ay, ax))

def main(stdscr):
    score = 0

    # Inicializace barevných párů a přiřazení do proměnných
    barva_hada, barva_jablicka, barva_prekazky = init_colors()

    # Nastavení režimu
    curses.curs_set(0)         # Skryjeme kurzor
    stdscr.nodelay(1)          # Vstup nebude blokující
    stdscr.timeout(100)        # Obnovovací interval 100 ms

    # Získání rozměrů obrazovky
    sh, sw = stdscr.getmaxyx()

    # Inicializace hada – počáteční pozice uprostřed
    head_y = sh // 2
    head_x = sw // 4
    snake = [(head_y, head_x)]
    key = curses.KEY_RIGHT

    # Vytvoření překážek a jablíček
    obstacles = init_obstacles(sw, sh, 100)
    apples = init_apples(sw, sh, obstacles, snake, 30)

    while True:
        stdscr.clear()

        # Vykreslení skóre, překážek, jablíček a hada
        draw_score(stdscr, score, sh, sw)
        draw_obstacles(stdscr, obstacles, barva_prekazky)
        draw_apples(stdscr, apples, barva_jablicka)
        draw_snake(stdscr, snake, barva_hada)
        stdscr.refresh()

        # Čtení vstupu – pokud není stisknuta žádná klávesa, vrátí -1
        next_key = stdscr.getch()
        if next_key != -1:
            key = next_key

        # Výpočet nové pozice hlavy podle stisknuté klávesy
        head_y, head_x = snake[-1]
        if key == curses.KEY_RIGHT:
            head_x += 1
        elif key == curses.KEY_LEFT:
            head_x -= 1
        elif key == curses.KEY_UP:
            head_y -= 1
        elif key == curses.KEY_DOWN:
            head_y += 1
        new_head = (head_y, head_x)

        # Kontrola kolize
        collision_msg = check_collision(new_head, snake, obstacles, sh, sw)
        if collision_msg:
            error_msg = f"{collision_msg} Score: {score}"
            stdscr.addstr(sh // 2, sw // 2 - len(error_msg) // 2,
                          error_msg, curses.A_BOLD | curses.A_BLINK)
            stdscr.refresh()
            time.sleep(2)
            break

        # Kontrola, zda had snědl jablko
        if new_head in apples:
            score += 1
            apples.remove(new_head)
            # Had roste – přidáme novou hlavu, ale neodstraňujeme ocas
            snake.append(new_head)
            generate_new_apple(sw, sh, obstacles, snake, apples)
        else:
            # Had se pohybuje – přidáme novou hlavu a odstraníme ocas
            snake.append(new_head)
            snake.pop(0)

        time.sleep(0.1)

while True:
    curses.wrapper(main)
