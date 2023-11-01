import pygame

def __init__():
  global match_start
  global match_end
  match_start = pygame.mixer.Sound("Match_Start.wav")
  match_end = pygame.mixer.Sound("Match_End.wav")
  
def play_match_start():
  pygame.mixer.Sound.play(match_start)

def play_match_end():
  pygame.mixer.Sound.play(match_end)
  
if __name__ == '__main__':
  import time
  
  pygame.init()
  __init__()
  play_match_start()
  time.sleep(5)
  play_match_end()
  time.sleep(5)
  pygame.quit()
  
