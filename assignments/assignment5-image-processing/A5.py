# CS 1400
# Assignment 5: Image Processing
# Written by Soojung Kim

from graphics import *
from random import *


# ---------------------------
# Example function: switch RGB values
# def switch_image_colors(image):
#     switched_image = image.clone()
#     for y in range(image.getHeight()):
#         for x in range(image.getWidth()):
#             color = image.getPixel(x, y)
#             new_color = [color[2], color[0], color[1]]
#             switched_image.setPixel(x, y, new_color)
#     return switched_image


# ---------------------------
# Grayscale
# by setting each pixel to a weighted average of RGB values.
def color_image_to_gray_scale(image):
    gray_image = image.clone()
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            r, g, b = image.getPixel(x, y)
            gray = int(0.299*r + 0.587*g + 0.114*b)
            gray_image.setPixel(x, y, [gray, gray, gray])
    return gray_image


# ---------------------------
# Black & White
# by applying a threshold to the grayscale intensity.
def color_image_to_black_and_white(image, threshold):
    bw_image = image.clone()
    gray_version = color_image_to_gray_scale(image)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            gray, _, _ = gray_version.getPixel(x, y)
            if gray >= threshold:
                bw_image.setPixel(x, y, [255, 255, 255])
            else:
                bw_image.setPixel(x, y, [0, 0, 0])
    return bw_image


# ---------------------------
# Sepia
# producing an old-fashioned brownish tone.
def sepia_image(image):
    sepia_img = image.clone()
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            r, g, b = image.getPixel(x, y)
            new_r = int(r*0.393 + g*0.769 + b*0.189)
            new_g = int(r*0.349 + g*0.686 + b*0.168)
            new_b = int(r*0.272 + g*0.534 + b*0.131)
            # clamp
            if new_r > 255: new_r = 255
            if new_g > 255: new_g = 255
            if new_b > 255: new_b = 255
            sepia_img.setPixel(x, y, [new_r, new_g, new_b])
    return sepia_img


# ---------------------------
# Rainbow Gradient
# by adjusting RGB values based on the vertical position of pixels.
def rainbow_gradient(image):
    rainbow_img = image.clone()
    height = image.getHeight()
    for y in range(height):
        for x in range(image.getWidth()):
            r, g, b = image.getPixel(x, y)
            ratio = y / height
            new_r = int(r * (1 - ratio))
            new_g = int(g * (1 - abs(2*ratio - 1)))
            new_b = int(b * ratio)
            rainbow_img.setPixel(x, y, [new_r, new_g, new_b])
    return rainbow_img


# ---------------------------
# Custom Filter (Warm Sunset Filter)
# boosting red/green values and reducing blue tones.
def custom_filter(image):
    custom_img = image.clone()
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            r, g, b = image.getPixel(x, y)
            new_r = int(min(r * 1.2, 255))   # boost red
            new_g = int(min(g * 1.1, 255))   # slightly boost green
            new_b = int(b * 0.8)             # reduce blue
            custom_img.setPixel(x, y, [new_r, new_g, new_b])
    return custom_img


# ---------------------------
# Green Screen Merge
# by replacing pure green pixels with background pixels.
def green_screen_image(foreground, background):
    merged = background.clone()
    for y in range(foreground.getHeight()):
        for x in range(foreground.getWidth()):
            r, g, b = foreground.getPixel(x, y)
            if r == 0 and g == 255 and b == 0:  # pure green
                merged.setPixel(x, y, background.getPixel(x, y))
            else:
                merged.setPixel(x, y, [r, g, b])
    return merged


# ---------------------------
# Pointillist
# then drawing small colored circles based on their RGB values.
def color_image_to_pointillist(image, win, num_points):
    width = image.getWidth()
    height = image.getHeight()
    for _ in range(num_points):
        x = randint(0, width-1)
        y = randint(0, height-1)
        r, g, b = image.getPixel(x, y)
        circle = Circle(Point(x, y), 3)
        circle.setFill(r, g, b)
        circle.setWidth(0)   # remove circle border
        circle.draw(win)


# ---------------------------
# Utility: Load and center image
def load_image(filename):
    image = Image(Point(0, 0), filename)
    image.move(int(image.getWidth() / 2), int(image.getHeight() / 2))
    return image


# ---------------------------
# Main function
def main():
    arches_image = load_image("Arches.png")
    cat_image = load_image("green-screen-cat.png")

    win = GraphWin('Image Art',
                   arches_image.getWidth(),
                   arches_image.getHeight(),
                   autoflush=False)

    arches_image.draw(win)
    win.getMouse()

    # Example test
    # switched_image = switch_image_colors(arches_image)
    # switched_image.draw(win)
    # win.getMouse()

    # Grayscale
    gray_image = color_image_to_gray_scale(arches_image)
    gray_image.draw(win)
    gray_image.save("gray.png")
    win.getMouse()

    # Black and White
    bw_image = color_image_to_black_and_white(arches_image, 100)
    bw_image.draw(win)
    bw_image.save("bw.png")
    win.getMouse()

    # Sepia
    sepia = sepia_image(arches_image)
    sepia.draw(win)
    sepia.save("sepia.png")
    win.getMouse()

    # Rainbow
    rainbow_image = rainbow_gradient(arches_image)
    rainbow_image.draw(win)
    rainbow_image.save("rainbow.png")
    win.getMouse()

    # Custom Filter
    custom_image = custom_filter(arches_image)
    custom_image.draw(win)
    custom_image.save("custom.png")
    win.getMouse()

    # Green Screen Merge
    merged_image = green_screen_image(cat_image, arches_image)
    merged_image.draw(win)
    merged_image.save("merged.png")
    win.getMouse()

    # Pointillist
    color_image_to_pointillist(arches_image, win, 25000)
    win.getMouse()

    win.close()


# ---------------------------
if __name__ == "__main__":
    main()
