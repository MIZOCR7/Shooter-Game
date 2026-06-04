import pygame
import os

pygame.init()

BG = (144, 201, 120)

WIDTH = 800
HEIGHT = int(WIDTH * 0.8)

GRAVITY = 0.75
TILE_SIZE = 40

RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

clock = pygame.time.Clock() 
FPS = 60

moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

bullet_img = pygame.image.load("assets/img/icons/bullet.png").convert_alpha()
grenade_img = pygame.image.load("assets/img/icons/grenade.png").convert_alpha()
health_box_img = pygame.image.load("assets/img/icons/health_box.png")
ammo_box_img = pygame.image.load("assets/img/icons/ammo_box.png")
grenade_box_img = pygame.image.load("assets/img/icons/grenade_box.png")
item_boxes = {
  "Health"     : health_box_img,
  "Ammo"      : ammo_box_img,
  "Grenade"    : grenade_box_img
}

font = pygame.font.SysFont("Futura", 30)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  WINDOW.blit(img, (x,y))
  



def draw_bg():
  WINDOW.fill(BG)
  pygame.draw.line(WINDOW, RED, (0, 300), (WIDTH, 300))
  pygame.display.update

class Soldier(pygame.sprite.Sprite):
  def __init__(self, x, y, character_type, scale, speed, ammo, grenades):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.character_type = character_type
    self.speed = speed
    self.ammo = ammo
    self.start_ammo = ammo
    self.grenades = grenades
    self.vel_y = 0
    self.direction = 1
    self.jump = False 
    self.shoot_cooldown = 0
    self.in_air = True
    self.flip = False
    self.health = 100
    self.max_health = self.health
    self.animation_list = []
    self.frame_index = 0  
    self.action = 0
    self.update_time = pygame.time.get_ticks()
    
    
    animation_types = ['idle', 'Run', 'Jump', "Death"] 
    for animation in animation_types:
      temp_list = []
      
      num_of_frames = len(os.listdir(f'assets/img/{self.character_type}/{animation}'))
      
      for i in range(num_of_frames):
        img = pygame.image.load(f'assets/img/{self.character_type}/{animation}/{i}.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        temp_list.append(img)  

      self.animation_list.append(temp_list)
    self.image = self.animation_list[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
  
  
  def update(self):
    self.update_animation()
    self.check_alive()
    if self.shoot_cooldown > 0:
      self.shoot_cooldown -= 1
  
  
  
  def move(self, moving_left, moving_right):
    
    dx = 0
    dy = 0
    
    if moving_left:
      dx = -self.speed
      self.flip = True
      self.direction = -1
    if moving_right:
      dx = self.speed
      self.flip = False
      self.direction = 1
    
    if self.jump == True and self.in_air == False:
      self.vel_y = -11
      self.jump = False
      self.in_air = True
    
    self.vel_y += GRAVITY 
    if self.vel_y > 10:
      self.vel_y = 10
    dy += self.vel_y
    
    if self.rect.bottom + dy > 300:
      dy = 300 - self.rect.bottom 
      self.in_air = False
      
    
    self.rect.x += dx
    self.rect.y += dy
  
  def shoot(self):
    if self.shoot_cooldown == 0 and self.ammo > 0:  
      self.shoot_cooldown = 20
      bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
      bullet_group.add(bullet)
      self.ammo -= 1
  
  def ai(self):
    if self.alive and player.alive:
      if self.direction == 1:
        ai_moving_right = True
      else:
        ai_moving_right = False
      ai_moving_left = not ai_moving_right
      self.move(ai_moving_left, ai_moving_right)
  
   
  def update_animation(self):
    ANIMATION_COOLDOWN = 100
    self.image = self.animation_list[self.action][self.frame_index]
    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1 
    if self.frame_index >= len(self.animation_list[self.action]):
      if self.action == 3:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
  
  def update_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()
  
  def check_alive(self):
    if self.health <= 0:
      self.health = 0
      self.speed = 0
      self.alive = False
      self.update_action(3)
      

  
  def draw(self):
    WINDOW.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    

class ItemBox(pygame.sprite.Sprite):
  def __init__(self, item_type, x , y):
    pygame.sprite.Sprite.__init__(self)
    self.item_type = item_type
    self.image = item_boxes[self.item_type]
    self.rect = self.image.get_rect()
    self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) 
    
    
  def update(self):
    if pygame.sprite.collide_rect(self, player):
      if self.item_type == "Health":
        player.health += 25
        if player.health > player.max_health:
          player.health = player.max_health
      elif self.item_type == "Ammo":
        player.ammo += 15
      elif self.item_type == "Grenade":
        player.grenades += 3
      self.kill()
    
    
class HealthBar():
  def __init__(self, x, y, health, max_health):
    self.x = x
    self.y = y
    self.health = health
    self.max_health = max_health
    
  def draw(self, health):
    self.health = health
    ratio = self.health / self.max_health
    pygame.draw.rect(WINDOW, BLACK, (self.x - 2, self.y - 2, 154, 24))
    pygame.draw.rect(WINDOW, RED, (self.x, self.y, 150, 20))
    pygame.draw.rect(WINDOW, GREEN, (self.x, self.y, 150 * ratio, 20)) 
    
    



class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y, direction):
    pygame.sprite.Sprite.__init__(self)
    self.speed = 10
    self.image = bullet_img
    self.rect = self.image.get_rect()  
    self.rect.center = (x,y)
    self.direction = direction
    
  def update(self):
    self.rect.x += (self.direction * self.speed)
    
    if self.rect.right < 0 or self.rect.left > WIDTH:
      self.kill()
      
    if pygame.sprite.spritecollide(player, bullet_group, False):
      if player.alive:
        player.health -= 5
        self.kill()
    
    for enemy in enemy_group:
      if pygame.sprite.spritecollide(enemy, bullet_group, False):
        if enemy.alive:
          enemy.health -= 25
          
          self.kill()


class Grenade(pygame.sprite.Sprite):
  def __init__(self, x, y, direction):
    pygame.sprite.Sprite.__init__(self)
    self.timer = 100
    self.vel_y = -11
    self.speed = 7
    self.image = grenade_img
    self.rect = self.image.get_rect()  
    self.rect.center = (x,y)
    self.direction = direction  
  
  def update(self):
    self.vel_y += GRAVITY
    dx = self.direction * self.speed
    dy = self.vel_y
    
    if self.rect.bottom + dy > 300:
      dy = 300 - self.rect.bottom
      self.speed = 0
    
    if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
      self.direction *= -1
      dx = self.direction * self.speed
      
    self.rect.x += dx
    self.rect.y += dy 
    
    self.timer -= 1
    if self.timer <= 0:
      self.kill()
      explosion = Explosion(self.rect.x, self.rect.y, 0.5)
      Explosion_group.add(explosion)
      
      if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
      abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
        player.health -= 50
        
      for enemy in enemy_group:
        if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
          enemy.health -= 50
      

class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y, scale):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for num in range(1,6):
      img = pygame.image.load(f'assets/img/explosion/exp{num}.png').convert_alpha()
      img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
      self.images.append(img)
    self.frame_index = 0
    self.image = self.images[self.frame_index]
    self.rect = self.image.get_rect()  
    self.rect.center = (x,y)
    self.counter = 0 
    
    
  def update(self):
    EXPLOSION_SPEED = 4
    
    self.counter += 1
    if self.counter >= EXPLOSION_SPEED:
      self.counter = 0
      self.frame_index += 1
      if self.frame_index >= len(self.images):
        self.kill()
      else:
        self.image = self.images[self.frame_index]
    
  


    
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()    
grenade_group = pygame.sprite.Group()    
Explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

item_box = ItemBox("Health", 100, 260)
item_box_group.add(item_box)
item_box = ItemBox("Ammo", 400, 260)
item_box_group.add(item_box)
item_box = ItemBox("Grenade", 500, 260)
item_box_group.add(item_box)
  
player = Soldier(200, 200, 'player', 1.65, 5, 20, 5) 
health_bar = HealthBar(10, 10, player.health, player.health)
enemy = Soldier(400, 200, "enemy", 1.65, 5, 3, 0)
enemy2 = Soldier(600, 200, "enemy", 1.65, 5, 3, 0) 

enemy_group.add(enemy) 
enemy_group.add(enemy2) 





run = True
while run:
  clock.tick(FPS)
  draw_bg()
  
  health_bar.draw(player.health)
  
  
  draw_text("AMMO: ", font, WHITE, 10, 35)
  for x in range(player.ammo):
    WINDOW.blit(bullet_img, (90 + (x * 10), 40))
  draw_text("Grenades: ", font, WHITE, 10, 60) 
  for x in range(player.grenades):
    WINDOW.blit(grenade_img, (135 + (x * 15), 60))
  
  
  player.update()
  player.draw()
  for enemy in enemy_group:
    enemy.update()
    enemy.draw()
  
  bullet_group.update()
  grenade_group.update()
  Explosion_group.update()
  item_box_group.update()
  bullet_group.draw(WINDOW)
  grenade_group.draw(WINDOW)
  Explosion_group.draw(WINDOW)
  item_box_group.draw(WINDOW)
  

  
  if player.alive:
    if shoot:
      player.shoot()
    elif grenade and grenade_thrown == False and player.grenades > 0:
      grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction) 
      grenade_group.add(grenade)
      player.grenades -= 1
      grenade_thrown = True
      
      
    if player.in_air:
      player.update_action(2)
    elif moving_left or moving_right:
      player.update_action(1)
    else:
      player.update_action(0)
  
  player.move(moving_left, moving_right)
  
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False
      
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_right = True
      if event.key == pygame.K_w and player.alive:
        player.jump = True
      if event.key == pygame.K_SPACE:
        shoot = True
      if event.key == pygame.K_q:
        grenade = True
        
    # release the key
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_right = False
      if event.key == pygame.K_SPACE:
        shoot = False
      if event.key == pygame.K_q:
        grenade = False
        grenade_thrown = False
    
  pygame.display.update()
  
pygame.quit() 



