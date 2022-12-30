import pygame
import time
import math
from utils import scale_image, blit_rotate_center
   
# load images
GRASS = scale_image(pygame.image.load("data/imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("data/imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("data/imgs/track-border.png"), 0.9)
FINISH = pygame.image.load("data/imgs/finish.png")
RED_CAR = scale_image(pygame.image.load("data/imgs/red-car.png"), 0.55)
GRENN_CAR = scale_image(pygame.image.load("data/imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60

def draw(win, imgs, player_car):
    for img, pos in imgs:
        win.blit(img, pos)
        
    player_car.draw(win)
    pygame.display.update()

class AbstractCar:
    IMG = RED_CAR
    
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 180
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel
    
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.x -= horizontal
        self.y -= vertical
        
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        
class PlayerCar(AbstractCar):         
    IMG = RED_CAR
    START_POS = (180, 200)
 
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0))]
player_car = PlayerCar(4, 4)
    
while run:
    # make sure that the while loop does not run faster than FPS
    clock.tick(FPS)
    
    draw(WIN, images, player_car)        
    
    for event in pygame.event.get():
        # if X button is pressed to close the window
        if event.type == pygame.QUIT:
            run = False
            break
        
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    
    if not moved:
        player_car.reduce_speed()
                        
pygame.quit()