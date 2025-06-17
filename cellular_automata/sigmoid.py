import pygame
import sys
from random import randint, uniform, random
import math
k = 1
populate = lambda n: [[uniform(0,1) for x in range(n)] for _ in range(n)]

def sigmoid(x, k=1, x0=4):
    # takes a number x and passes it through a sigmoid curve, which outputs a value between 0 and 1
    return 1 / (1 + math.exp(-k * (x - x0)))

def apply_rule(matrix, y, x, k=0.1):
    '''
    it adds up the 8 neighboring cell values around position (y, x),
    and uses a sigmoid function to convert the sum into a probability p
    IF THE SUM IS::
    1. near 4 (the center x0), p ≈ 0.5.
    2. much less than 4, p is close to 0.
    3. much more than 4, p is close to 1.

    a random number between 0 and 1 is generated.
    if it's less than p, return 1 (cell becomes alive) else die
    '''
    theSum = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y-1][x+1] + matrix[y][x-1] + matrix[y][x+1] + matrix[y+1][x-1] + matrix[y+1][x] + matrix[y+1][x+1]
    # P from sig centered at 4
    p = sigmoid(theSum, k=k, x0=4)
    return 1 if random() < p else 0


### normie code ahead

WIDTH, HEIGHT = 700, 700
running = True
grid_len = 100
cell_size = 3
offset = 50
fps = 7

color1 = (222, 239, 183)
color2 = (110, 222, 138)
color3 = (37, 162, 68)
color4 = (21, 93, 39)

matrix = populate(grid_len)
new_matrix = [[0]*grid_len for _ in range(grid_len)]

pygame.init()
pygame.key.set_repeat(10, 10)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("celuauto")

while running:
    screen.fill(color3)
    for y in range(1, grid_len-1):
        for x in range(1, grid_len-1):
            new_matrix[y][x] = apply_rule(matrix, y, x, k)
            if new_matrix[y][x]:
                pygame.draw.circle(screen, color4, (offset+(cell_size*2*x)+(cell_size+0.5), offset+(cell_size*2*y)+(cell_size+0.5)), cell_size+1)
                pygame.draw.circle(screen, color2, (offset+(cell_size*2*x), offset+(cell_size*2*y)), cell_size+1)

    matrix = new_matrix
    new_matrix = [[0]*grid_len for _ in range(grid_len)]

    pygame.display.flip()
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                matrix = populate(grid_len)
        #elif event.type == pygame.K
            if event.key == pygame.K_RIGHT:
                k += 0.01
            if event.key == pygame.K_LEFT:
                k -= 0.01
pygame.quit()
sys.exit()
