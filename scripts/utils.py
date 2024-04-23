import os
import pygame

BASE_IMG_PATH = 'sprites/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,255,0))
    return img