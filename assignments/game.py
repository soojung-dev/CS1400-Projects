# Adventure Game Project - CS 1400
# Authors: Soojung Kim
# Date: Dec 2025

import pygame
import sys
import level1
import level2
import level3
import display_win_or_loss

# --------------------------------- Global Settings ---------------------------------
WIDTH, HEIGHT = 1280, 960
FPS = 60


def show_start_screen(screen):
    """
    Display the START screen with a background image and a clickable START button.

    The game begins only when the user clicks the button. Closing the window here
    exits the entire program.

    :param screen: Pygame display Surface created in main()
    """

    clock = pygame.time.Clock()

    # reference: PyGame font.SysFont() docs:
    # https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
    font = pygame.font.SysFont(None, 80)

    # --------------------------------- Background Image ---------------------------------
    # Load a dark city background and scale it to fill the entire window.
    bg_img = pygame.image.load("start_dark_city.jpg").convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

    # --------------------------------- START Button ---------------------------------
    # Render the "START" label and use its rect to define a rounded button area.
    text_surface = font.render("START", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 300))
    button_rect = text_rect.inflate(80, 40)

    running = True
    while running:
        # ----------------------------- Event Handling -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Left mouse click to start the game if clicked inside button_rect.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # reference: Rect.collidepoint() docs:
                # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collidepoint
                if button_rect.collidepoint(event.pos):
                    running = False

        # ----------------------------- Drawing -----------------------------
        # Draw background image.
        screen.blit(bg_img, (0, 0))

        # Draw rounded START button and text.
        pygame.draw.rect(screen, (230, 230, 230), button_rect, border_radius=20)
        pygame.draw.rect(screen, (180, 180, 180), button_rect, 4, border_radius=20)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    """
    Main entry point of the game.

    Initializes Pygame, shows the start screen once, then runs Level 1, Level 2,
    and Level 3 in sequence. After each level, a win or loss screen is displayed
    using display_win_or_loss. The game exits after the final screen is shown.
    """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cat Night Walk")

    # --------------------------------- Start Screen ---------------------------------
    # Show the START screen once before entering Level 1.
    show_start_screen(screen)

    # --------------------------------- Level 1 ---------------------------------
    # Run Level 1. If the level returns False, show loss screen and exit.
    passed_level1 = level1.level1(screen)
    if not passed_level1:
        display_win_or_loss.display_loss_screen(screen)
        pygame.quit()
        sys.exit()
    else:
        # If Level 1 is cleared, briefly show a win screen before Level 2.
        display_win_or_loss.display_win_screen(screen)

    # --------------------------------- Level 2 ---------------------------------
    passed_level2 = level2.level2(screen)
    if not passed_level2:
        display_win_or_loss.display_loss_screen(screen)
        pygame.quit()
        sys.exit()
    else:
        display_win_or_loss.display_win_screen(screen)

    # --------------------------------- Level 3 ---------------------------------
    passed_level3 = level3.level3(screen)
    if not passed_level3:
        display_win_or_loss.display_loss_screen(screen)
        pygame.quit()
        sys.exit()
    else:
        display_win_or_loss.display_final_screen(screen)


if __name__ == "__main__":
    main()