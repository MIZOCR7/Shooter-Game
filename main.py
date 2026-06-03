import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False

pygame.quit() 
