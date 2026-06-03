import pygame

pygame.init()

WIDTH = 800
HEIGHT = int(WIDTH * 0.8)


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

class Soldier(pygame.sprite.Sprite):
  def __init__(self, x, y, scale):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('assets/img/player/idle/0.png')
    self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
  
  def draw(self):
    WINDOW.blit(self.image, self.rect)
    
player = Soldier(200, 200, 3)






run = True
while run:
  
  
  player.draw()
  
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False
  pygame.display.update()
  
pygame.quit() 
