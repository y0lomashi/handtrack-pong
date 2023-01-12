import pygame
import pygame_menu
from pygame_menu import themes
import settings as s

# initialize game
pygame.init()

# setup display
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 1000, 720
screen = pygame.display.set_mode(DISPLAY_SIZE)

# set window caption
pygame.display.set_caption("Handtracking Pong by Curtis Li")


# menu function
def set_difficulty(value, difficulty):
    # Default difficulty
    s.p2_type = "human"
    if difficulty == 0:
        s.p2_type = "random"
    if difficulty == 1:
        s.p2_type = "following"
    if difficulty == 2:
        s.p2_type = "human"


def menu():

    def start_the_game():
        # import play file and play game because it is not in function
        import play

    def dif_menu():
        mainmenu._open(level)

    mainmenu = pygame_menu.Menu("Welcome",
                                1000,
                                720,
                                theme=themes.THEME_SOLARIZED)
    mainmenu.add.text_input("Name: ", default="username", maxchar=20)
    mainmenu.add.button("Play", start_the_game)
    mainmenu.add.button("Difficulty", dif_menu)
    mainmenu.add.button("Quit", pygame_menu.events.EXIT)

    level = pygame_menu.Menu("Select a Difficulty",
                             1000,
                             720,
                             theme=themes.THEME_BLUE)
    level.add.selector("Difficulty :", [("Easy", 0), ("Human", 2),
                                        ("Hard", 1)],
                       onchange=set_difficulty)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(screen)

        pygame.display.update()


menu()
