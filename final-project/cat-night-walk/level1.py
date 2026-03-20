# Adventure Game Project - CS 1400
# Authors: Soojung Kim
# Date: Dec 2025

import pygame


def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check pixel-perfect collision between two masked surfaces.

    :param mask1: Mask of the first object (for example, the player)
    :param rect1: Rect of the first object
    :param mask2: Mask of the second object (for example, walls or enemy)
    :param rect2: Rect of the second object
    :return: True if any opaque pixels overlap, otherwise False
    """

    # Compute relative offset between the two rects
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]

    # reference: PyGame mask.overlap docs:
    # https://www.pygame.org/docs/ref/mask.html#pygame.mask.Mask.overlap
    # If overlap() returns a point, there is a collision; otherwise, None
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap is not None


def level1(screen):
    """
    Run Level 1 where the cat navigates through the maze.

    This level uses the display Surface created in game.py and does not
    create or destroy the window. The level starts immediately without
    any extra start button inside Level 1.

    :param screen: display Surface created in game.py (shared window)
    :return: True if the cat reaches the goal,
             False on wall/enemy collision or when the user closes the window.
    """

    clock = pygame.time.Clock()

    # --------------------------------- Background (Maze) ---------------------------------
    # Load the maze image and use its rect size for boundary and collision.
    map_surface = pygame.image.load("level1_maze.png").convert_alpha()
    map_rect = map_surface.get_rect()
    map_size = map_rect.size

    # reference: PyGame set_caption() docs:
    # https://www.pygame.org/docs/ref/display.html?highlight=caption#pygame.display.set_caption
    # Set the window title for this level.
    pygame.display.set_caption("Level 1 - Dark Alley Maze")

    # reference: PyGame threshold() docs:
    # https://www.pygame.org/docs/ref/transform.html#pygame.transform.threshold
    # Create a mask from the maze image: we treat near-white pixels as walls.
    wall_color = (255, 255, 255, 255)
    map_mask = pygame.mask.from_threshold(
        map_surface,
        wall_color,
        (10, 10, 10, 255)
    )

    # --------------------------------- Cat (Main Character) ---------------------------------
    # Load and scale the player sprite (cat).
    cat_base = pygame.image.load("player_cat.png").convert_alpha()
    cat_base = pygame.transform.scale(cat_base, (120, 90))

    # reference for sprite flipping:
    # https://www.pygame.org/docs/ref/transform.html#pygame.transform.flip
    # Prepare two versions for left/right facing directions.
    cat_right = cat_base
    cat_left = pygame.transform.flip(cat_base, True, False)

    # Start facing right at the initial spawn point inside the maze.
    cat = cat_right
    cat_rect = cat.get_rect()
    cat_rect.center = (190, 140)
    cat_speed = 4.5

    # Mask for pixel-perfect collision of the cat sprite.
    cat_mask = pygame.mask.from_surface(cat_right)

    # --------------------------------- Dog (Enemy) ---------------------------------
    # Load enemy sprite (dog) and create a shared mask.
    enemy_surface = pygame.image.load("enemy_dog.png").convert_alpha()
    enemy_surface = pygame.transform.scale(enemy_surface, (80, 80))
    enemy_mask = pygame.mask.from_surface(enemy_surface)

    # Horizontal movement bounds for enemies (same lane width for both).
    enemy_left_bound = 150
    enemy_right_bound = 1150

    # reference: PyGame Rect docs -> midleft, midright:
    # https://www.pygame.org/docs/ref/rect.html?highlight=midtop
    # Enemy 1 (second corridor, moves left → right).
    enemy1_rect = enemy_surface.get_rect()
    enemy1_rect.midleft = (enemy_left_bound, 320)

    # Enemy 2 (third corridor, moves right → left).
    enemy2_rect = enemy_surface.get_rect()
    enemy2_rect.midright = (enemy_right_bound, 620)

    # Each enemy is stored as a dict so we can keep speed and bounds together.
    # Two lane dogs patrolling horizontally; touching them resets the level.
    enemies = [
        {
            "surf": enemy_surface,
            "rect": enemy1_rect,
            "mask": enemy_mask,
            "speed": 5,  # positive speed → moves to the right
            "left": enemy_left_bound,
            "right": enemy_right_bound,
        },
        {
            "surf": enemy_surface,
            "rect": enemy2_rect,
            "mask": enemy_mask,
            "speed": -5,  # negative speed → moves to the left
            "left": enemy_left_bound,
            "right": enemy_right_bound,
        },
    ]

    # --------------------------------- Goal ---------------------------------
    # Load and scale the goal icon; reaching this ends the level successfully.
    end_img = pygame.image.load("goal.png").convert_alpha()
    end_img = pygame.transform.scale(end_img, (70, 70))
    end_rect = end_img.get_rect()
    end_rect.center = (185, 880)

    # --------------------------------- Game Loop ---------------------------------
    is_playing = True
    while is_playing:
        # --------------------- Event Handling ---------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Do not quit pygame here; just signal failure to main().
                return False

        # --------------------- Player Movement ---------------------
        # code from ChatGPT in response to: "how to add keyboard movement and flip sprites left/right"
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

        # Keep the cat inside the maze image boundaries.
        if cat_rect.left < 0:
            cat_rect.left = 0
        if cat_rect.right > map_size[0]:
            cat_rect.right = map_size[0]
        if cat_rect.top < 0:
            cat_rect.top = 0
        if cat_rect.bottom > map_size[1]:
            cat_rect.bottom = map_size[1]

        # --------------------- Wall Collision ---------------------
        # If the cat overlaps with wall pixels in the maze mask, the level fails.
        if pixel_collision(cat_mask, cat_rect, map_mask, map_rect):
            return False

        # --------------------- Enemy Movement & Collision ---------------------
        for enemy in enemies:
            rect = enemy["rect"]

            # Move enemy horizontally by its speed.
            rect.x += enemy["speed"]

            # code from ChatGPT (asked: "how to ensure enemy speed flips direction reliably?")
            # abs() makes the value always positive, and -abs() always negative.
            # Reverse direction at the left boundary.
            if rect.left <= enemy["left"]:
                rect.left = enemy["left"]
                enemy["speed"] = abs(enemy["speed"])  # ensure it moves right (positive)

            # Reverse direction at the right boundary.
            elif rect.right >= enemy["right"]:
                rect.right = enemy["right"]
                enemy["speed"] = -abs(enemy["speed"])  # ensure it moves left (negative)

            # Check pixel-perfect collision between the cat and this enemy.
            if pixel_collision(cat_mask, cat_rect, enemy["mask"], rect):
                return False

        # --------------------- Goal Check ---------------------
        # If the cat reaches the goal icon, the level is cleared.
        # reference: Rect.colliderect() docs:
        # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
        if cat_rect.colliderect(end_rect):
            return True

        # --------------------------------- Drawing ---------------------------------
        # Clear the screen, draw maze background, goal, enemies, and cat.
        screen.fill((255, 255, 255))
        screen.blit(map_surface, map_rect)
        screen.blit(end_img, end_rect)

        for enemy in enemies:
            screen.blit(enemy["surf"], enemy["rect"])

        screen.blit(cat, cat_rect)

        pygame.display.update()
        clock.tick(60)
