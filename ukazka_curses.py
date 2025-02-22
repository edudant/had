import curses

def main(stdscr):
    # Nastavení: Skryjeme blikající kurzor pro lepší vzhled
    curses.curs_set(0)
    
    # Vyčistíme obrazovku, abychom měli "čisté plátno"
    stdscr.clear()
    
    # Inicializujeme barevný režim (pokud váš terminál barvy podporuje)
    curses.start_color()
    
    # Získáme aktuální rozměry obrazovky (počet řádků a sloupců)
    height, width = stdscr.getmaxyx()
    
    # Inicializace barevného páru číslo 1: červený text na černém pozadí
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)

    # Připravíme text, který chceme zobrazit
    text = f"Ahoj, curses! Výška: {height} Šířka: {width}"
    
    # Vypočítáme pozici pro centrování textu
    x = width // 2  - len(text) // 2 
    y = height // 2
    
    # Vykreslíme text na vypočítané pozici (souřadnice: řádek y, sloupec x)
    stdscr.addstr(y, x, text, curses.color_pair(1))
    
    # Aktualizujeme obrazovku, aby se vykreslený text objevil
    stdscr.refresh()
    
    # Program čeká na stisk klávesy, než se ukončí
    stdscr.getch()

# Funkce curses.wrapper se postará o:
#   • Inicializaci curses (nastavení režimu terminálu, apod.)
#   • Zavolání naší funkce main s hlavním oknem (stdscr)
#   • Obnovení původního stavu terminálu po skončení programu
curses.wrapper(main)
