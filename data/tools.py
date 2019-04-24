import pygame
import os

# monokai color palette
WHITE = (253, 250, 243)
BLACK = (45, 43, 46)
RED = (255, 96, 137)
GREEN = (169, 220, 199)
BLUE = (119, 220, 230)
YELLOW = (255, 216, 102)
ORANGE = (252, 151, 105)
PURPLE = (171, 157, 244)

images = {}
sounds = {}
fonts = {}

def load_images(directory, colorkey=(0, 0, 0), extensions=('.png', '.jpg', '.bmp')):
    """Loads all images with the specified file extensions.

    Args:
        directory (str): Path to the directory that contains the files.
        colorkey  (tup): Used to set colorkey if no alpha transparency is found in image.
        extensions (tup): The file extensions accepted by the function.

    Returns:
        images (dict): The loaded images.
    """
    #images = Assets.images
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
    #sounds = Assets.sounds
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
    #fonts = Assets.fonts
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
    """Draws text in rectangle to surface."""
    text_font = pygame.font.Font(font, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def clear_text(font, color, text, size, x, y, screen):
    """Covers text with solid rectangle to surface."""
    text_font = pygame.font.Font(font, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.fill(color, text_rect)

def draw_progress_bar(x, y, progress, screen):
    """Draw a colored progress bar with outline to surface."""
    BAR_LENGTH = 40
    BAR_HEIGHT = 400

    progress = max(progress, 0)
    fill = (progress / 100) * BAR_HEIGHT
    fill_rect = pygame.Rect(x, y, BAR_LENGTH, fill)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    pygame.draw.rect(screen, GREEN, outline_rect)
    pygame.draw.rect(screen, WHITE, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 4)

def play_music(track):
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)

def play_sound(sound):
    snd = pygame.mixer.Sound(sound)
    snd.play()