import pygame
pygame.init()
pygame.mixer.init() #to play music
pygame.mixer_music.set_volume(0.1)
def play_music (file : str): 
    pygame.mixer.music.load(file)  #play music when the game is running
    pygame.mixer.music.play(-1)  #-1 loop the music


def play_sound_fx(file: str):
    sound = pygame.mixer.Sound(file)  # Load sound as a Sound object
    sound.play()  # Play without interrupting background music

def stop_sound() : 
    pygame.mixer.music.stop() #stop music
