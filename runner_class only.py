import pygame
import math
from sys import exit
from random import randint, choice

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Chicken Little')
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False

start_time = 0
score = 0
bg_x = 0

#bg_music = pygame.mixer.Sound('audio/music.wav')
#bg_music.set_volume(0.1)
#bg_music.play(loops = -1)

sky_surface = pygame.transform.scale(pygame.image.load('graphics/plx-1.png').convert_alpha(),(800, 400))
ground_surface = pygame.image.load('graphics/ground-1.png').convert_alpha()
ground_width = ground_surface.get_width()
ground_height = ground_surface.get_height()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#to store character images
		self.player_walk = []
		for i in range(1,11):
			player_walk_image = pygame.transform.scale(pygame.image.load(f"graphics/player/ChikBoy_run{i}.png").convert_alpha(),(84, 84))
			self.player_walk.append(player_walk_image)

		self.player_index = 0
		self.player_jump = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_jump.png').convert_alpha(),(84, 84))
		

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))
		self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= (SCREEN_HEIGHT - ground_height):
			self.gravity = -20
			#self.jump_sound.play()
		if keys[pygame.K_RIGHT] and self.rect.right <= SCREEN_WIDTH - (SCREEN_WIDTH * 1/10):
			self.rect.x += 2.5
		if keys[pygame.K_LEFT] and self.rect.right >= SCREEN_WIDTH * 1/10:
			self.rect.x -= 2.5
		
		#for event in pygame.event.get():
		#	if event.type == pygame.KEYDOWN :
		#		if event.key == pygame.K_DOWN :
		#			self.image = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_crouch.png').convert_alpha(),(84, 50))
		#			self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))

		#	if event.type == pygame.KEYUP :
		#		if event.key == pygame.K_DOWN :
		#			self.image = self.player_walk[0]
		#			self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))

		#add crouch
		#if keys[pygame.K_DOWN] and self.rect.bottom == (SCREEN_HEIGHT - ground_height):
		#	self.image = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_crouch.png').convert_alpha(),(84, 50))
		#	self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))
		#elif not keys[pygame.K_DOWN] and self.gravity==0:
		#	self.image = self.player_walk[0]
		#	self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= (SCREEN_HEIGHT - ground_height):
			self.rect.bottom = (SCREEN_HEIGHT - ground_height)

	def animation_state(self):
		if self.rect.bottom < (SCREEN_HEIGHT - ground_height): 
			self.image = self.player_jump

		else:
			self.player_index += 0.3
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = (SCREEN_HEIGHT - ground_height) - 90
		elif type == 'snail':
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = (SCREEN_HEIGHT - ground_height)
		else:
			snake_1 = pygame.transform.scale(pygame.image.load('graphics/snake/Snake1.png').convert_alpha(),(50, 50))
			snake_2 = pygame.transform.scale(pygame.image.load('graphics/snake/Snake2.png').convert_alpha(),(50, 50))
			self.frames = [snake_1,snake_2]
			y_pos  = (SCREEN_HEIGHT - ground_height) + 5


		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


scroll = 0
bg_images = []

bg_theme_1 = pygame.transform.scale(pygame.image.load("graphics/background_theme1.png").convert_alpha(),(800, 400))
bg_theme_2 = pygame.transform.scale(pygame.image.load("graphics/background_theme2_2.png").convert_alpha(),(800, 400))
bg_theme_3 = pygame.transform.scale(pygame.image.load("graphics/background_theme3.png").convert_alpha(),(800, 400))
bg_theme_4 = pygame.transform.scale(pygame.image.load("graphics/background_theme4.png").convert_alpha(),(800, 400))

tiles_1 = math.ceil(SCREEN_WIDTH / bg_theme_1.get_width()) + 2
bg_rect = bg_theme_1.get_rect()

bg_images.append(bg_theme_1)
bg_images.append(bg_theme_1)

def draw_bg():
	for x, i in enumerate(bg_images):
		screen.blit(i, ((x * bg_theme_1.get_width()) + bg_x, 0))
		#bg_rect.x = x  * bg_theme_1.get_width() + bg_x
		#pygame.draw.rect(screen, (255,0,0), bg_rect,1)


ground_tile = math.ceil(SCREEN_WIDTH / ground_surface.get_width()) + 2
print(ground_tile)
def draw_ground():
  for x in range(0, ground_tile):
    screen.blit(ground_surface, ((x * ground_width) + bg_x, SCREEN_HEIGHT - ground_height))

# Intro screen
player_stand = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run1.png').convert_alpha(),(84, 84))
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Chicken Little',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

theme = 1

#Game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				if theme == 1:
					obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
				elif theme == 2:
					obstacle_group.add(Obstacle(choice(['snake'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:

		draw_bg()
		score = display_score()

		bg_x -= 4 
		if abs(bg_x)> bg_theme_1.get_width():
			del bg_images[0]
			if score < 10:
				bg_images.append(bg_theme_1)
				theme = 1
			elif score < 20:
				bg_images.append(bg_theme_2)
				theme = 2
			elif score < 30:
				bg_images.append(bg_theme_3)
				them = 3
			else:
				bg_images.append(bg_theme_4)
				theme = 4
			bg_x = 0

		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)
		bg_x = 0

		theme = 1
		bg_images.clear()
		bg_images.append(bg_theme_1)
		bg_images.append(bg_theme_1)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(FPS)