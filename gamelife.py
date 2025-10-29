import numpy as np
import pygame, sys
from pygame.locals import *

# ================= Pattern Definitions =================
glider_gun = np.array([
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])

glider = np.array([
    [0,1,0],
    [0,0,1],
    [1,1,1]
])

blinker_h = np.array([[1,1,1]])
blinker_v = np.array([[1],[1],[1]])
block = np.array([[1,1],[1,1]])

# Lightweight Spaceship (LWS)
lws = np.array([
    [0,1,1,1,1],
    [1,0,0,0,1],
    [0,0,0,0,1],
    [1,0,0,1,0]
])

# Pulsar (大脈衝星)
pulsar = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,1,0,0,0,1,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,1,0,0,0,1,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,1,0,0,0,1,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,1,0,0,0,1,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
])

# Beacon (烽火)
beacon = np.array([
    [1,1,0,0],
    [1,1,0,0],
    [0,0,1,1],
    [0,0,1,1]
])

# ================= Game Settings =================
W = 120
H = 80
CELL_SIZE = 8
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 15

Z = np.zeros((H,W), dtype=int)

# ================= Game of Life Rules =================
def compute_neighbours(Z):
    N = np.zeros(Z.shape, dtype=int)
    for y in range(1,H-1):
        for x in range(1,W-1):
            N[y,x] = np.sum(Z[y-1:y+2,x-1:x+2]) - Z[y,x]
    return N

def iterate(Z):
    N = compute_neighbours(Z)
    newZ = Z.copy()
    for y in range(1,H-1):
        for x in range(1,W-1):
            if Z[y,x] == 1 and (N[y,x] < 2 or N[y,x] > 3):
                newZ[y,x] = 0
            elif Z[y,x] == 0 and N[y,x] == 3:
                newZ[y,x] = 1
    return newZ

# ================= Place Patterns =================
def place_glider_gun():
    yy, xx = 5, 5
    h, w = glider_gun.shape
    Z[yy:yy+h, xx:xx+w] = glider_gun

def place_pattern(pattern, top_left_y, top_left_x):
    h, w = pattern.shape
    Z[top_left_y:top_left_y+h, top_left_x:top_left_x+w] = pattern

# ================= Pygame Init =================
pygame.init()
screen = pygame.display.set_mode((W*CELL_SIZE,H*CELL_SIZE))
pygame.display.set_caption("Game of Life - Black & White")
clock = pygame.time.Clock()

# ================= 初始化畫面 =================
place_glider_gun()
place_pattern(glider, 20, 20)
place_pattern(blinker_h, 35, 30)
place_pattern(blinker_v, 40, 50)
place_pattern(block, 60, 40)
#place_pattern(lws, H-10, 5)  # 可選擇放置下方太空船
place_pattern(beacon, 30, 70)

# 放置多個大脈衝星
pulsar_positions = [
    (10, 85),
    (25, 80),
    (50, 15),
    (65, 10)
]
for py, px in pulsar_positions:
    place_pattern(pulsar, py, px)

# ================= Game Loop =================
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_g:
                place_glider_gun()

    Z = iterate(Z)

    screen.fill(BLACK)
    for y in range(H):
        for x in range(W):
            if Z[y,x] == 1:
                pygame.draw.rect(screen, WHITE, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.update()
    clock.tick(FPS)