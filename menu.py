import pygame
import pygame_menu
from pygame_menu import themes
import json
import settings as s

# initialize game
pygame.init()

# setup display
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 1000, 650
screen = pygame.display.set_mode(DISPLAY_SIZE)

# set window caption
pygame.display.set_caption("Handtracking Pong by Curtis Li")

# Load scores for leaderboard
try:
    with open(s.filepath, 'r') as f:
        scores = json.load(f)
except FileNotFoundError:
    scores = {}
scores_sorted = sorted([(p, s) for p, s in scores.items()],
                       reverse=True,
                       key=lambda x: x[1])


# menu function
def set_difficulty(value, difficulty):
    # Default difficulty
    s.p2_type = "following"
    if difficulty == 0:
        s.p2_type = "random"
    if difficulty == 1:
        s.p2_type = "following"
    if difficulty == 2:
        s.p2_type = "human"


def username(name):
    # on input change your value is returned here
    s.username = name


def menu():

    def start_the_game():
        # import play file and play game because it is not in function
        import play

    def dif_menu():
        mainmenu._open(level)

    def lead_menu():
        mainmenu._open(leaderboard)

    mainmenu = pygame_menu.Menu("Welcome",
                                1000,
                                650,
                                theme=themes.THEME_SOLARIZED)
    mainmenu.add.text_input("Name: ",
                            default="player 1",
                            maxchar=20,
                            onchange=username)
    mainmenu.add.button("Play", start_the_game)
    mainmenu.add.button("Difficulty", dif_menu)
    mainmenu.add.button("Leaderboard", lead_menu)
    mainmenu.add.button("Quit", pygame_menu.events.EXIT)

    level = pygame_menu.Menu("Select a Difficulty",
                             1000,
                             650,
                             theme=themes.THEME_BLUE)
    level.add.selector("Difficulty :", [("Easy", 0), ("Hard", 1),
                                        ("Human", 2)],
                       onchange=set_difficulty)
    leaderboard = pygame_menu.Menu("Leaderboard",
                                   1000,
                                   650,
                                   theme=themes.THEME_BLUE)
    leaderboard.add.label("Leaderboard")
    rank = 1
    for player, score in scores_sorted:
        if rank > 5:
            break
        else:
            leaderboard.add.button(
                f"|{str(rank).ljust(3)}|{str(player).ljust(21)}|{str(score).rjust(3)}|",
                align=pygame_menu.locals.ALIGN_CENTER,
                font_name=pygame.font.SysFont("FreeMono, Monospace", 26))
            # leaderboard.add_text_label(f"| {str(rank).ljust(3)} | {str(player).ljust(22)} | {str(score).ljust(5)} |", align=pygame_menu.locals.ALIGN_CENTER)
            rank += 1

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(screen)

        pygame.display.update()


if __name__ == "__main__":  # If this file is run directly
    menu()
