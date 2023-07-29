import pygame
from pygame.sprite import Group, Group
import random

pygame.init()

clock = pygame.time.Clock()

WIDTH = 500
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Comet")

#BACKGROUND VARIABLES
bg = pygame.image.load("bg.png")
x = 0
y = 0
x1 = 0
y1 = -HEIGHT

button_img = pygame.image.load("button_img.png")

game_over = False

def reset_game():
    global game_over
    game_over = False
    comet.rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
    comet.vel = 0

    enemy_group.empty()

    global y, y1
    y = 0
    y1 = -HEIGHT

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
class Comet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        #UPDATE THE BACKGROUND IMAGE
        for num in range (1, 5):
            img = pygame.image.load(f"comet_img{num}.png").convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        #FRICTION VARIABLES
        self.vel = 0
        self.friction = 0.09

    def update(self):
        self.counter += 1
        comet_cooldown = 5
        if game_over == False:
            if self.counter > comet_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
    #APPLY THE FRICTION ON SPRITE
        self.vel *= (1.0 - self.friction)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.vel -= 2
            if pygame.mouse.get_pressed()[2] == 1:
                self.vel += 2

        self.rect.x += self.vel
    #SET THE BOUNDARIES OF SCREEN
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vel *= -0.5
        if self.rect.right >= 500:
            self.rect.right = 500
            self.vel *= -0.5

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img = pygame.image.load(f"enemy_img{num}.png").convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.counter += 1
        enemy_cooldown = 5

        if self.counter > enemy_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        self.rect.y += 5

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        if self.rect.bottom < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                game_over = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
    def get_size(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=self.rect.center)

comet_group = pygame.sprite.Group()
comet = Comet(WIDTH // 2, HEIGHT // 2 + 100)
comet_group.add(comet)

enemy_group = pygame.sprite.Group()

#CREATE A TIMER OF 1 SECOND FOR GENERATE ENEMIES
event_user = pygame.USEREVENT + 0
pygame.time.set_timer(event_user, 1000)

button = Button(WIDTH // 2, HEIGHT // 2, button_img)
button.get_size(button.image.get_width() * 4, button.image.get_height() * 4)

run = True
while run:
    clock.tick(60)

#SCROLL THE BACKGROUND
    y1 += 5
    y += 5
    screen.blit(bg, (x, y))
    screen.blit(bg, (x1, y1))
    if y > HEIGHT:
         y = -HEIGHT
    if y1 > HEIGHT:
        y1 = -HEIGHT
#DRAW SPRITES ON THE SCREEN
    comet_group.draw(screen)
    comet_group.update()
        
    enemy_group.draw(screen)
    enemy_group.update()

    if pygame.sprite.groupcollide(comet_group, enemy_group, False, False):
        game_over = True

#CHECK FOR EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #RANDOM GENERATE OF ENEMIES
        if game_over == False:
            if event.type == event_user:
                enemy = Enemies(random.randint(50, WIDTH - 50), HEIGHT // 2 - 250)
                enemy_group.add(enemy)

    if game_over == True:
        y1 = 0
        y = 0
        
        button.draw(screen)
        if button.draw(screen):
            reset_game()

    pygame.display.update()

pygame.quit()