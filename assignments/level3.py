# Adventure Game Project - CS 1400
# Authors: Soojung Kim
# Date: Dec 2025

import pygame
import random


def level3(screen):
    """
    Run Level 3, a stealth-style stage in the restaurant storage room.

    The cat must collect all tuna cans while avoiding being caught by the chef.
    When the chef is facing the cat, the cat cannot move outside the safe zone.
    Moving while watched results in failure; eating all tuna cans results in success.

    This level uses the shared display Surface created in game.py and
    does not create or destroy its own window.

    :param screen: Pygame display Surface passed from game.py
    :return: True if the cat eats all tuna cans, False if caught or window is closed.
    """

    clock = pygame.time.Clock()
    screen_rect = screen.get_rect()
    width, height = screen_rect.size

    # SAFE_X defines a vertical strip on the left where movement is always safe
    SAFE_X = 80
    safe_zone_rect = pygame.Rect(0, 0, SAFE_X, height)

    # ----------------------------- Background -----------------------------
    # Load the background image for the storage room.
    bg = pygame.image.load("level3_restaurant_storage_room.jpg").convert()

    # reference: PyGame set_caption() docs:
    # https://www.pygame.org/docs/ref/display.html?highlight=caption#pygame.display.set_caption
    pygame.display.set_caption("Level 3 - Chef's Storage Stealth")

    # ----------------------------- Images -----------------------------
    # Load all sprites: cat, chef (front/back), and tuna cans.
    cat_img = pygame.image.load("player_cat.png").convert_alpha()
    chef_front_img = pygame.image.load("chef_front.png").convert_alpha()
    chef_back_img = pygame.image.load("chef_back.png").convert_alpha()
    tuna_img = pygame.image.load("tuna.png").convert_alpha()

    # Smoothly scale sprites to the desired sizes.
    cat_img = pygame.transform.smoothscale(cat_img, (120, 90))
    chef_front_img = pygame.transform.smoothscale(chef_front_img, (140, 160))
    chef_back_img = pygame.transform.smoothscale(chef_back_img, (140, 160))
    tuna_img = pygame.transform.smoothscale(tuna_img, (80, 50))

    # ----------------------------- Positions -----------------------------
    # Initial position: cat starts on the left side of the screen.
    cat_rect = cat_img.get_rect()
    cat_rect.center = (60, height // 2)

    # Chef stands near the right side, facing the cat or turning around.
    chef_rect = chef_front_img.get_rect()
    chef_rect.center = (1150, height // 2)

    cat_speed = 5

    # ----------------------------- Random Tuna Cans -----------------------------
    # Randomly place tuna cans in the room without overlapping each other
    # and without overlapping the cat or the chef.
    tuna_rects = []
    num_tuna = 8  # adjustable number of tuna cans

    tw, th = tuna_img.get_rect().size

    tuna_min_x = int(150)
    tuna_max_x = int(1020)
    tuna_min_y = int(height * 0.15)
    tuna_max_y = int(height * 0.85)

    # code from ChatGPT (prompt: "pygame randomly place items without overlap")
    # reference: Rect.colliderect() docs:
    # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
    for _ in range(num_tuna):
        for attempt in range(100):
            tx = random.randint(tuna_min_x, tuna_max_x - tw)
            ty = random.randint(tuna_min_y, tuna_max_y - th)
            tr = pygame.Rect(tx, ty, tw, th)

            # Avoid overlapping the cat or the chef.
            if tr.colliderect(cat_rect) or tr.colliderect(chef_rect):
                continue

            # Avoid overlapping already placed tuna cans.
            if any(tr.colliderect(t) for t in tuna_rects):
                continue

            tuna_rects.append(tr)
            break

    # ----------------------------- Chef state (Red-Light / Green-Light logic) -----------------------------
    # facing_cat = True  → chef is looking at the cat (movement is dangerous).
    # facing_cat = False → chef has turned away (cat can move freely).
    facing_cat = False
    timer = 0.0
    look_back_duration = 2.5   # chef looking away duration
    look_front_duration = 1.2  # chef watching duration

    # ----------------------------- Game Loop -----------------------------
    running = True
    while running:

        # reference: PyGame Clock.tick() docs:
        # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
        # dt is the elapsed time in seconds since the last frame.
        dt = clock.tick(60) / 1000.0

        # ----------------------------- Event Handling -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # ----------------------------- Movement Input -----------------------------
        # code from ChatGPT in response to:
        # "how to add keyboard movement and flip sprites left/right"
        # (same movement logic as in Level 1 and Level 2, reused for consistency)
        # reference: PyGame keyboard docs:
        # https://www.pygame.org/docs/ref/key.html
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx -= cat_speed
        if keys[pygame.K_RIGHT]:
            dx += cat_speed
        if keys[pygame.K_UP]:
            dy -= cat_speed
        if keys[pygame.K_DOWN]:
            dy += cat_speed

        # ----------------------------- Chef Timing (Toggle Facing State) -----------------------------
        # code from ChatGPT (prompt: "pygame red light green light style timing with toggle state")
        # The chef alternates between looking away and looking at the cat.
        timer += dt
        if facing_cat:
            # Chef is currently facing the cat; after look_front_duration, turn away.
            if timer >= look_front_duration:
                facing_cat = False
                timer = 0.0
        else:
            # Chef is currently turned away; after look_back_duration, turn to face the cat.
            if timer >= look_back_duration:
                facing_cat = True
                timer = 0.0

        # ----------------------------- Apply Cat Movement -----------------------------
        cat_rect.x += dx
        cat_rect.y += dy

        # reference: Rect.clamp_ip() docs:
        # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.clamp_ip
        # Keep the cat inside the screen boundaries.
        cat_rect.clamp_ip(screen_rect)

        moved = (dx != 0 or dy != 0)

        # If the chef is facing the cat and the cat moves outside the safe zone, the player fails.
        if facing_cat and moved and not safe_zone_rect.colliderect(cat_rect):
            return False

        # ----------------------------- TUNA EAT (Collect Tuna) -----------------------------
        # Remove any tuna rect that collides with the cat.
        for tr in tuna_rects[:]:  # iterate over a copy to allow removal
            if cat_rect.colliderect(tr):
                tuna_rects.remove(tr)

        # ----------------------------- SUCCESS CHECK -----------------------------
        # If there are no tuna cans left, the level is cleared.
        if len(tuna_rects) == 0:
            return True

        # ----------------------------- Drawing -----------------------------
        # Draw background first.
        screen.blit(bg, (0, 0))

        # Draw all remaining tuna cans.
        for tr in tuna_rects:
            screen.blit(tuna_img, tr)

        # Draw the chef depending on whether he is facing the cat or not.
        if facing_cat:
            screen.blit(chef_front_img, chef_rect)
        else:
            screen.blit(chef_back_img, chef_rect)

        # Draw the player cat.
        screen.blit(cat_img, cat_rect)

        pygame.display.flip()