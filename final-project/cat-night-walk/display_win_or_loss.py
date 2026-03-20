# Adventure Game Project - CS 1400
# Authors: Soojung Kim
# Date: Dec 2025

import pygame
import sys


# --------------------------------- Loss Screen ---------------------------------
def display_loss_screen(screen):
    """
    Display the loss screen with a black background and red 'YOU LOSE' text.

    The screen remains visible until any key is pressed. Closing the window
    exits the entire program.

    :param screen: Pygame display Surface passed from main()
    """

    # Fill background with black
    screen.fill((0, 0, 0))

    # reference: PyGame SysFont docs:
    # (same logic as in game, reused for consistency)
    # https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
    font = pygame.font.SysFont(None, 100)

    # Render loss message
    text = font.render("YOU LOSE", True, (255, 0, 0))
    rect = text.get_rect(center=(640, 480))

    screen.blit(text, rect)
    pygame.display.flip()

    wait_for_key()


# --------------------------------- Win Screen ---------------------------------
def display_win_screen(screen):
    """
    Display the win screen with a white background and blue 'YOU WIN' text.

    The screen remains visible until any key is pressed. Closing the window
    exits the entire program.

    :param screen: Pygame display Surface passed from main()
    """

    # Fill background with white
    screen.fill((255, 255, 255))

    # reference: PyGame SysFont docs:
    # https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
    font = pygame.font.SysFont(None, 100)

    # Render win message
    text = font.render("YOU WIN", True, (0, 0, 255))
    rect = text.get_rect(center=(640, 480))

    screen.blit(text, rect)
    pygame.display.flip()

    wait_for_key()


def display_final_screen(screen):
    """
    Display the final ending screen showing the cat's tuna feast after all
    three levels are cleared.

    The screen remains visible until any key is pressed. Closing the window
    exits the entire program.

    :param screen: Pygame display Surface passed from main()
    """

    # --------------------------------- Load Background ---------------------------------
    # Background showing the cat celebrating with collected tuna cans.
    # (Use your own chosen image file)
    bg = pygame.image.load("final_cat_feast.jpg").convert()
    bg = pygame.transform.scale(bg, (1280, 960))

    # reference: PyGame set_caption() docs:
    # https://www.pygame.org/docs/ref/display.html?highlight=caption#pygame.display.set_caption
    pygame.display.set_caption("Ending")

    # reference: PyGame SysFont docs:
    # https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
    font = pygame.font.SysFont(None, 70)

    # Main ending message
    text = font.render("You survived the night and earned a great feast!", True, (255, 255, 255))
    rect = text.get_rect(center=(640, 850))

    # --------------------------------- Draw ---------------------------------
    screen.blit(bg, (0, 0))
    screen.blit(text, rect)
    pygame.display.flip()

    # Wait for user input
    wait_for_key()


# --------------------------------- Key Wait Handler ---------------------------------
def wait_for_key():
    """
    Wait until the user presses any key.
    Window close events immediately terminate the program.

    This function is used by both the win and loss screens.
    """

    # reference: PyGame event loop docs:
    # https://www.pygame.org/docs/ref/event.html#pygame.event.get
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Any key press continues to the next action
            if event.type == pygame.KEYDOWN:
                waiting = False
