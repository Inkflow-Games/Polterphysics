import pygame
pygame.init()
pygame.mixer.init() #to play music

def play_music (file : str):
    if not pygame.mixer.get_busy() : 
        
        pygame.mixer.music.load(file)  #play music when the game is running
        pygame.mixer.music.play(-1)  #-1 loop the music
    else :
        stop_sound() 
        pygame.mixer.music.load(file)  #play music when the game is running
        pygame.mixer.music.play(-1) #-1 loop the music


def play_sound_fx(file: str):
    sound = pygame.mixer.Sound(file)  # Load sound as a Sound object
    sound.play()  # Play without interrupting background music

def stop_sound() : 
    pygame.mixer.music.stop() #stop music
