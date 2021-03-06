"""Tools

This module contains helper functions and
variables for the game, especially in relation to assets.
"""


import os

import pygame


# asset folder paths
IMG_DIR = os.path.join('assets', 'images')
SND_DIR = os.path.join('assets', 'sounds')
FNT_DIR = os.path.join('assets', 'fonts')

# asset dictionaries
images = {}
sounds = {}
fonts = {}

# colors
WHITE = (253, 250, 243)
BLACK = (56, 54, 57)
RED = (255, 96, 137)
GREEN = (169, 220, 199)
BLUE = (119, 220, 230)


def change_icon(filename):
    """Changes the icon of the display window.

    Args:
        filename (str): The filename of the icon in the images directory, including the extension.
    """
    icon = pygame.image.load(os.path.join(IMG_DIR, filename))
    icon = icon.convert_alpha()
    pygame.display.set_icon(icon)


def load_images(directory, colorkey=(0, 0, 0), extensions=('.png', '.jpg', '.bmp')):
    """Loads all images with the specified file extensions.

    Args:
        directory (str): Path to the directory that contains the files.
        colorkey  (tup): Used to set colorkey if no alpha transparency is found in image.
        extensions (tup): The file extensions accepted by the function.

    Returns:
        images (dict): The loaded images.
    """
    for img in os.listdir(directory):
        name, ext = os.path.splitext(img)
        if ext in extensions:
            img = pygame.image.load(os.path.join(directory, img))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            images[name] = img
    return images


def load_sounds(directory, extensions=('.ogg', '.mp3', '.wav', '.mdi')):
    """Loads all sounds with the specified file extensions.

    Args:
        directory (str): Path to the directory that contains the files.
        extensions (tup): The file extensions accepted by the function.

    Returns:
        sounds (dict): The loaded images.
    """
    for snd in os.listdir(directory):
        name, ext = os.path.splitext(snd)
        if ext in extensions:
            sounds[name] = os.path.join(directory, snd)
    return sounds


def load_fonts(directory, extensions=('.ttf')):
    """Loads all fonts with the specified file extension.

    Args:
        directory (str): Path to the directory that contains the files.
        extensions (tup): The file extensions accepted by the function.

    Returns:
        fonts (dict): The loaded fonts.
    """
    for fnt in os.listdir(directory):
        name, ext = os.path.splitext(fnt)
        if ext in extensions:
            fonts[name] = os.path.join(directory, fnt)
    return fonts


def render_image(image, screen_size, screen):
    """Renders an image to the screen at the size of the window.

    Args:
        image (obj): Image that has been loaded by the game.
        screen_size (tup): The width and height of the screen.
        screen (obj): The surface to render the image on.
    Returns:
        image (obj): Image that has been scaled to the screen size.
    """
    if image.get_size() != screen_size:
        image = pygame.transform.smoothscale(image, screen_size, screen)
    return image


def render_text(font, color, text, size, x, y, screen):
    """Draws text in rectangle to surface.

    Args:
        font (str): Name of font.
        color (tup): RGB color code.
        text (str): The text to be displayed.
        size (int): Size of the text.
        x (int): X-axis coordinate of text rectangle.
        y (int): Y-axis coordinate of text rectangle.
        screen (obj): Surface to draw text on.
    """
    text_font = pygame.font.Font(font, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def clear_text(font, color, text, size, x, y, screen):
    """Covers text with solid rectangle to surface.

    Args:
        font (str): Use same font as the text to be covered.
        color (tup): RGB color code. Use same color as background.
        text (str): Use the same text that you are covering.
        size (int): Use the same size as the rendered text.
        x (int): Use same X-axis coordinate as the rendered text.
        y (int): Use same Y-axis coordinate as the rendered text.
        screen (obj): Surface to draw rectangle on.
    """
    text_font = pygame.font.Font(font, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.fill(color, text_rect)


def draw_progress_bar(x, y, progress, screen):
    """Draw a colored progress bar with outline to surface.

    Args:
        x (int): X-axis coordinate to draw the bar.
        y (int): Y-axis coordinate to draw the bar.
        progress (int): Completion progress of the task.
        screen (obj): Surface to render bar on.
    """
    bar_length = 40
    bar_height = 400
    progress = max(progress, 0)
    fill = (progress / 100) * bar_height
    fill_rect = pygame.Rect(x, y, bar_length, fill)
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    pygame.draw.rect(screen, GREEN, outline_rect)
    pygame.draw.rect(screen, WHITE, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 4)


def play_music(track):
    """Plays a music sound on infinite loop.

    Args:
        track (str): Name of the music track to play.
    """
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)


def play_sound(sound):
    """Plays a sound once.

    Args:
        sound (str): Name of the sound to play.
    """
    snd = pygame.mixer.Sound(sound)
    snd.play()
