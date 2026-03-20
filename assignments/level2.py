# Adventure Game Project - CS 1400
# Authors: Soojung Kim
# Date: Dec 2025

import pygame, random


def level2(screen):
    """
    Run Level 2 where the cat moves upward across a road while avoiding
    falling dog obstacles. Touching a dog results in failure, and reaching
    the goal icon at the top clears the level.

    This level uses the shared display Surface created in game.py.

    :param screen: Pygame display Surface passed from game.py
    :return: True if the cat reaches the goal,
             False on collision with a dog or window close.
    """

    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # --------------------------------- Background (Road Image) ---------------------------------
    # Load the road image and use it as the scrolling background for this level.
    road_img = pygame.image.load("level2_road.jpg").convert()
    road_rect = road_img.get_rect()

    # reference: PyGame set_caption() docs:
    # (same movement logic as in Level 1, reused for consistency)
    # https://www.pygame.org/docs/ref/display.html?highlight=caption#pygame.display.set_caption
    # Set the window title for this level.
    pygame.display.set_caption("Level 2 - Midnight Road Crossing")

    # --------------------------------- Player (Cat) ---------------------------------
    # Use the same cat sprite as Level 1, but start near the bottom of the road.
    cat_base = pygame.image.load("player_cat.png").convert_alpha()
    cat_base = pygame.transform.scale(cat_base, (120, 90))

    # reference for sprite flipping:
    # (same movement logic as in Level 1, reused for consistency)
    # https://www.pygame.org/docs/ref/transform.html#pygame.transform.flip
    # Prepare two versions for left/right facing directions.
    cat_right = cat_base
    cat_left = pygame.transform.flip(cat_base, True, False)

    cat = cat_right
    cat_rect = cat.get_rect()
    cat_rect.center = (65, 910)
    cat_speed = 4

    # --------------------------------- Goal Area (Top of Screen) ---------------------------------
    # Visual goal band at the top of the screen to indicate the safe area.
    goal_height = 80
    goal_rect = pygame.Rect(0, 0, width, goal_height)
    goal_color = (170, 210, 250)

    # --------------------------------- Falling Dogs (Obstacles) ---------------------------------
    # Dogs drop from the top of the screen and act as obstacles.
    dog_img = pygame.image.load("enemy_dog.png").convert_alpha()
    dog_img = pygame.transform.scale(dog_img, (80, 80))

    dog_width, dog_height = dog_img.get_width(), dog_img.get_height()
    dogs = []  # list of active falling dog rects

    # code from ChatGPT (prompt: "how to spawn enemies on a timer in pygame")
    # reference: PyGame USEREVENT docs:
    # https://www.pygame.org/docs/ref/event.html?highlight=userevent
    # Use a custom PyGame event to spawn dogs at timed intervals.
    DOG_EVENT = pygame.USEREVENT + 1

    # reference: PyGame set_timer() docs:
    # https://www.pygame.org/docs/ref/time.html?highlight=set_timer#pygame.time.set_timer
    # Timer is disabled at first and will be enabled after the countdown.
    pygame.time.set_timer(DOG_EVENT, 0)
    dog_speed = 8

    # --------------------------------- Goal Icon Image ---------------------------------
    # Goal icon that the cat must touch to clear the level.
    end_img = pygame.image.load("goal.png").convert_alpha()
    end_img = pygame.transform.scale(end_img, (70, 70))
    end_rect = end_img.get_rect()
    end_rect.center = (1200, 100)

    # --------------------------------- 3-2-1-GO Countdown ---------------------------------
    font_count = pygame.font.SysFont(None, 150)

    def draw_scene_with_text(text_str):
        """
        Render the full scene (background, goal area, goal icon, cat) and
        overlay a centered countdown text.

        :param text_str: text to display at the center of the screen ("3", "2", "1", "GO")
        """
        # Draw background and static elements first.
        screen.blit(road_img, (0, 0))
        pygame.draw.rect(screen, goal_color, goal_rect)
        screen.blit(end_img, end_rect)
        screen.blit(cat, cat_rect)

        # code from StackOverflow (center countdown text on the screen):
        # https://stackoverflow.com/questions/68315636/pygame-center-text-in-moving-rect
        text_surface = font_count.render(text_str, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    # code from ChatGPT (prompt: "pygame countdown 3-2-1 go before game starts")
    # reference: PyGame time.get_ticks() docs:
    # https://www.pygame.org/docs/ref/time.html?highlight=time%20get_ticks#pygame.time.get_ticks
    # Display "3", "2", "1", and "GO" for 1 second each before the level starts.
    for text in ["3", "2", "1", "GO"]:
        start_time = pygame.time.get_ticks()
        counting = True
        while counting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            now = pygame.time.get_ticks()
            if now - start_time >= 1000:
                counting = False

            draw_scene_with_text(text)
            clock.tick(60)

    # After the countdown ends, enable the dog spawn timer (every 0.9 seconds).
    pygame.time.set_timer(DOG_EVENT, 900)
    level_started = True

    # --------------------------------- Main Game Loop ---------------------------------
    is_playing = True
    while is_playing:

        # ----------------------------- Event Handling (quit, spawning) -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Do not quit pygame here; signal failure and let main() handle it.
                return False

            if event.type == DOG_EVENT and level_started:
                # Spawn a new dog at a random x-position above the top edge.
                spawn_x = random.randint(0, width - dog_width)
                rect = dog_img.get_rect()
                # reference: PyGame Rect docs -> midtop:
                # https://www.pygame.org/docs/ref/rect.html?highlight=midtop
                rect.midtop = (spawn_x, -10)
                dogs.append(rect)

        # ----------------------------- Player Movement -----------------------------
        # code from ChatGPT in response to: "how to add keyboard movement and flip sprites left/right"
        # (same movement logic as in Level 1, reused for consistency)
        # reference: PyGame keyboard docs:
        # https://www.pygame.org/docs/ref/key.html
        # Keyboard movement (WASD / arrow keys) with sprite flipping.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            cat_rect.x -= cat_speed
            cat = cat_left
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            cat_rect.x += cat_speed
            cat = cat_right
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            cat_rect.y -= cat_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            cat_rect.y += cat_speed

        # Keep the cat inside the screen boundaries.
        if cat_rect.left < 0:
            cat_rect.left = 0
        if cat_rect.right > width:
            cat_rect.right = width
        if cat_rect.top < 0:
            cat_rect.top = 0
        if cat_rect.bottom > height:
            cat_rect.bottom = height

        # ----------------------------- Game Logic (movement, collision, win) -----------------------------
        if level_started:
            # code from ChatGPT (prompt: "manage multiple enemy rectangles in a list and move them down")
            # Move all falling dogs downward each frame.
            for r in dogs:
                r.y += dog_speed

            # Remove dogs that fall off the bottom of the screen.
            dogs = [r for r in dogs if r.top <= height]

            # reference: Rect.colliderect() docs:
            # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
            # Collision check: if any dog collides with the cat, the level fails.
            for r in dogs:
                if r.colliderect(cat_rect):
                    return False

            # If the cat reaches the goal icon, the level is cleared.
            if cat_rect.colliderect(end_rect):
                return True

        # --------------------------------- Drawing ---------------------------------
        # Draw background, goal area, goal icon, all dogs, and then the player.
        screen.blit(road_img, (0, 0))
        pygame.draw.rect(screen, goal_color, goal_rect)
        screen.blit(end_img, end_rect)

        # Draw all falling dogs.
        for r in dogs:
            screen.blit(dog_img, r)

        # Draw the player cat.
        screen.blit(cat, cat_rect)

        pygame.display.update()
        clock.tick(60)

    # Safety return (should normally exit via success/failure above).
    return False