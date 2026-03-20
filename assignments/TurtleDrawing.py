import turtle

# -----------------------------------------------------------------------------
# CS1400 – Assignment 2: Turtle Art
# Starter enhanced & completed by Soojung Kim and Junghee Kim
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Provided example from class (use this in draw_wall)
# -----------------------------------------------------------------------------

def draw_square(sq_turtle, side):
    """Draw one square with the given side length using the provided turtle."""
    for _ in range(4):
        sq_turtle.forward(side)
        sq_turtle.left(90)


# -----------------------------------------------------------------------------
# Utility helpers (optional, but handy for clean code)
# -----------------------------------------------------------------------------

def jump_to(j_turtle, x, y):
    """Move the turtle to (x, y) without drawing."""
    j_turtle.penup()
    j_turtle.goto(x, y)
    j_turtle.pendown()


def set_style(st_turtle, pencolor=None, pensize=None, speed=None, fillcolor=None):
    """Convenience: set common style properties if provided."""
    if pencolor is not None:
        st_turtle.pencolor(pencolor)
    if pensize is not None:
        st_turtle.pensize(pensize)
    if speed is not None:
        st_turtle.speed(speed)
    if fillcolor is not None:
        st_turtle.fillcolor(fillcolor)


# -----------------------------------------------------------------------------
# 1) draw_wall(wall_turtle, x, y, height)
# -----------------------------------------------------------------------------

def draw_wall(wall_turtle, x, y, height):
    """Draw a horizontal row of 5 blocks (squares) starting near (x, y).

    - wall_turtle: the turtle to draw with
    - x, y: starting location for the first square (lower-left corner)
    - height: side length for each square

    Uses a loop to draw 5 squares with a small gap between them and calls
    the provided draw_square() for each block.
    """
    gap = max(10, int(height * 0.3))  # reasonable gap that scales with size

    # Start at lower-left corner of the first block
    jump_to(wall_turtle, x, y)

    for _ in range(5):
        draw_square(wall_turtle, height)
        wall_turtle.penup()
        wall_turtle.forward(height + gap)
        wall_turtle.pendown()


# -----------------------------------------------------------------------------
# 2) Faces – draw_face + hair/ear variants
# -----------------------------------------------------------------------------

def draw_face(face_turtle, x, y, size=100, hair_style="spiky"):
    """Draw an emoji-like face centered at (x, y).

    Includes: head, two eyes, a curved mouth, hair, and ears.
    Extra parameter: hair_style in {"spiky", "round"}.
    """
    r = size * 0.5                  # head radius
    eye_r = size * 0.05             # eye radius
    eye_dx = size * 0.22            # eye horizontal offset
    eye_dy = size * 0.10            # eye vertical offset

    # --- Head -----------------------------------------------------------------
    set_style(face_turtle, pencolor="black", pensize=2, fillcolor="#FFD39B")
    face_turtle.penup(); face_turtle.goto(x, y - r); face_turtle.setheading(0)
    face_turtle.pendown(); face_turtle.begin_fill(); face_turtle.circle(r); face_turtle.end_fill()

    # --- Ears (optional but nice) --------------------------------------------
    draw_ears(face_turtle, x, y, size)

    # --- Eyes -----------------------------------------------------------------
    set_style(face_turtle, fillcolor="black")
    face_turtle.penup(); face_turtle.goto(x - eye_dx, y + eye_dy - eye_r)
    face_turtle.pendown(); face_turtle.begin_fill(); face_turtle.circle(eye_r); face_turtle.end_fill()

    face_turtle.penup(); face_turtle.goto(x + eye_dx, y + eye_dy - eye_r)
    face_turtle.pendown(); face_turtle.begin_fill(); face_turtle.circle(eye_r); face_turtle.end_fill()

    # --- Mouth (smile arc) ---------------------------------------------------
    mouth_r = size * 0.42
    face_turtle.penup(); face_turtle.goto(x - mouth_r * 0.6, y - size * 0.12)
    face_turtle.setheading(-60); face_turtle.pendown(); face_turtle.circle(mouth_r, 120)
    face_turtle.penup()

    # --- Hair -----------------------------------------------------------------
    if hair_style.lower() == "spiky":
        draw_hair_spiky(face_turtle, x, y, size)
    else:
        draw_hair_round(face_turtle, x, y, size)


def draw_ears(t, x, y, size):
    """Small filled semicircle ears positioned relative to the head."""
    r = size * 0.5
    ear_r = size * 0.12
    set_style(t, pencolor="black", fillcolor="#FFD39B", pensize=2)

    # Left ear
    t.penup(); t.goto(x - r * 0.85, y + r * 0.15); t.setheading(120)
    t.pendown(); t.begin_fill(); t.circle(ear_r, 200); t.end_fill(); t.penup()

    # Right ear (mirror)
    t.penup(); t.goto(x + r * 0.85, y + r * 0.15); t.setheading(60)
    t.pendown(); t.begin_fill(); t.circle(-ear_r, 200); t.end_fill(); t.penup()


def draw_hair_spiky(t, x, y, size):
    """Spiky hair using short repeated strokes across the top."""
    set_style(t, pencolor="saddlebrown", pensize=3)
    t.penup(); t.goto(x - size * 0.25, y + size * 0.5); t.setheading(90); t.pendown()
    for _ in range(7):
        t.forward(size * 0.22)
        t.backward(size * 0.22)
        t.right(12)
    t.penup()


def draw_hair_round(t, x, y, size):
    """Rounded bangs centered on top of head (robust, no drift)."""
    set_style(t, pencolor="saddlebrown", fillcolor="saddlebrown", pensize=2)
    base_x = x - size * 0.22
    base_y = y + size * 0.46
    for i in range(4):
        # Place each tile explicitly to avoid diagonal drift
        t.penup(); t.goto(base_x + i * size * 0.16, base_y)
        t.setheading(0)
        t.pendown(); t.begin_fill()
        t.setheading(180); t.circle(size * 0.12, 180)
        t.setheading(0); t.forward(size * 0.24)
        t.end_fill()
        t.penup()




# -----------------------------------------------------------------------------
# 3) Letters and word "DOG"
# -----------------------------------------------------------------------------

def draw_letter_D(t, x, y, height=120):
    """Letter D: clear D (left vertical + right semicircle)."""
    radius = height / 2
    set_style(t, pencolor="blue", pensize=10)
    # Left vertical
    t.penup(); t.goto(x, y); t.setheading(90); t.pendown()
    t.forward(height)
    # Semicircle bulging right: start at top, head east, draw CW 180°
    t.setheading(0)
    t.circle(-radius, 180)
    t.penup()


def draw_letter_O(t, x, y, height=120):
    """Letter O: full circle centered in a height-by-height box from (x, y)."""
    r = height/2
    cx, cy = x + r, y + r
    set_style(t, pencolor="orange", pensize=10)
    t.penup(); t.goto(cx, cy - r); t.setheading(0); t.pendown()
    t.circle(r)
    t.penup()


def draw_letter_G(t, x, y, height=120):
    """Letter G: full O with a long inward horizontal bar (clearly a G)."""
    r = height/2
    cx, cy = x + r, y + r
    set_style(t, pencolor="green", pensize=10)
    # Outer circle
    t.penup(); t.goto(cx + r, cy); t.setheading(120); t.pendown()
    t.circle(r, 330)
    # Inward bar from the rightmost point toward center
    t.penup(); t.goto(cx + r, cy - r * 0.5); t.setheading(180); t.pendown()
    t.forward(r * 0.55)
    t.penup()



def draw_word(t, x, y):
    """Write the word 'DOG' left-to-right using the letter helpers."""
    spacing = 160
    draw_letter_D(t, x, y, 120)
    draw_letter_O(t, x + spacing, y, 120)
    draw_letter_G(t, x + spacing * 2, y + 27, 120)


# -----------------------------------------------------------------------------
# main – create screen/turtle and call your functions
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(width=900, height=700)
    screen.title("CS1400 – Turtle Art (Assignment 2)")

    drawing_turtle = turtle.Turtle()
    set_style(drawing_turtle, speed=0)  # fastest for quick rendering

    # 1) Wall (choose coordinates that keep everything on-screen)
    draw_wall(drawing_turtle, x=-320, y=-220, height=50)

    # 2) Two faces (different hair styles and sizes)
    draw_face(drawing_turtle, x=-130, y=140, size=120, hair_style="spiky")
    draw_face(drawing_turtle, x=230,  y=100, size=80,  hair_style="round")

    # 3) Word (choose a readable location)
    draw_word(drawing_turtle, x=-260, y=-20)

    # Keep window open until closed by the user
    turtle.done()