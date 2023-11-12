import pygame

def init():
  global match_start
  global match_end
  global match_abort
  global match_win
  match_start = pygame.mixer.Sound("Match_Start.wav")
  match_end = pygame.mixer.Sound("Match_End.wav")
  match_abort = pygame.mixer.Sound("Match_Abort.wav")
  match_win = pygame.mixer.Sound("Match_Win.wav")
  
def play_match_start():
  pygame.mixer.Sound.play(match_start)

def play_match_end():
  pygame.mixer.Sound.play(match_end)
  
def play_match_abort():
  pygame.mixer.Sound.play(match_abort)

def play_match_win():
  pygame.mixer.Sound.play(match_win)
  
if __name__ == '__main__':
  import time
  
  pygame.init()
  init()
  play_match_start()
  time.sleep(5)
  play_match_end()
  time.sleep(5)
  pygame.quit()
  
