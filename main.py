import pygame
import sys
import numpy as np
import random

# # constants
cell_size = 30
cell_num = 20
board_size = cell_size*cell_num  # pixels
STEP = 1

# # init pygame
pygame.init()
screen = pygame.display.set_mode((board_size,board_size))
clock = pygame.time.Clock()

class fruit_class:
    def __init__(self):
        # place in the middle
        self.x = int(cell_num / 2)
        self.y = int(cell_num / 2)
        # load images
        self.image = pygame.image.load('images/apple.png').convert_alpha()

    def draw(self):
        screen.blit(self.image, ( int(self.x*cell_size), int(self.y*cell_size)) )

    def update(self, sneak_body):
        shuffle_again = True
        while shuffle_again:
            self.x = random.randint(0, cell_num-1)
            self.y = random.randint(0, cell_num-1)
            if not self.check_collision(sneak_body):
                shuffle_again = False

    def check_collision(self, sneak_body):
        is_collide = False
        for loc in sneak_body:
            if self.x == loc[0] and self.y == loc[1]:
                is_collide = True
                break
        return is_collide

class sneak_class:
    def __init__(self):
        self.pos = np.asarray([(2, 3), (2, 4), (2, 5)])
        self.direction = np.asarray((+1, 0))
        self.len = len(self.pos)

        self.head_up = pygame.image.load('images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('images/body_bl.png').convert_alpha()

    def draw(self):
        if False:
            # primitive method (rectangle)
            for loc in self.pos:
                pygame.draw.rect(screen, (226,150,100), pygame.Rect(loc[0], loc[1], cell_size, cell_size) )
        else:
            pixels_pos = cell_size * self.pos
            # tail
            tail_vec = self.pos[1,:] - self.pos[0,:]
            if tail_vec[0]==0:
                if   tail_vec[1] == 1:
                    screen.blit(self.tail_down, (pixels_pos[0, 0], pixels_pos[0, 1]))  # going down
                else:
                    screen.blit(self.tail_up, (pixels_pos[0, 0], pixels_pos[0, 1]))  # going up
            elif tail_vec[0] == 1:
                screen.blit(self.tail_right, (pixels_pos[0, 0], pixels_pos[0, 1]))  # going right
            else:
                screen.blit(self.tail_left, (pixels_pos[0, 0], pixels_pos[0, 1]))  # going left


            # head
            head_vec = self.pos[-2, :] - self.pos[-1, :]
            if head_vec[0] == 0:
                if head_vec[1] == 1:
                    screen.blit(self.head_up, (pixels_pos[-1, 0], pixels_pos[-1, 1]))  # going up
                else:
                    screen.blit(self.head_down, (pixels_pos[-1, 0], pixels_pos[-1, 1]))  # going down
            elif head_vec[0] == 1:
                screen.blit(self.head_left, (pixels_pos[-1, 0], pixels_pos[-1, 1]))  # going left
            else:
                screen.blit(self.head_right, (pixels_pos[-1, 0], pixels_pos[-1, 1]))  # going right

            nStop = self.len - 1
            for ind in range(1,nStop):
                vPrv = self.pos[ind, :] - self.pos[ind - 1, :]
                vNxt = self.pos[ind + 1, :] - self.pos[ind, :]

                if vPrv[0] == 1: # before went right
                    if   vNxt[0] == 1: # next went right
                        screen.blit(self.body_horizontal, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[1] == 1:  # next went down
                        screen.blit(self.body_bl, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[1] == -1:  # next went up
                        screen.blit(self.body_tl, (pixels_pos[ind, 0], pixels_pos[ind, 1]))

                elif vPrv[0] == -1: # before went left
                    if   vNxt[0] == -1: # next went left
                        screen.blit(self.body_horizontal, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[1] == 1:  # next went down
                        screen.blit(self.body_br, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[1] == -1:  # next went up
                        screen.blit(self.body_tr, (pixels_pos[ind, 0], pixels_pos[ind, 1]))

                elif vPrv[1] == 1:  # before went down
                    if   vNxt[0] == 1:  # next went right
                        screen.blit(self.body_tr, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[1] == 1:  # next went down
                        screen.blit(self.body_vertical, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[0] == -1:  # next went left
                        screen.blit(self.body_tl, (pixels_pos[ind, 0], pixels_pos[ind, 1]))

                elif vPrv[1] == -1:  # before went up
                    if vNxt[0] == 1:  # next went right
                        screen.blit(self.body_br, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[1] == -1:  # next went up
                        screen.blit(self.body_vertical, (pixels_pos[ind, 0], pixels_pos[ind, 1]))
                    elif vNxt[0] == -1:  # next went left
                        screen.blit(self.body_bl, (pixels_pos[ind, 0], pixels_pos[ind, 1]))

    def get_body(self):
        return self.pos

    def move(self, eat=False):
        head = self.pos[-1] + self.direction*STEP
        if eat:
            self.pos = np.vstack([self.pos, head])
            self.len += 1
        else:
            self.pos[:-1] = self.pos[1:]
            self.pos[-1] = head

    def is_alive(self):
        status = True
        #boundary = board_size - cell_size
        boundary = cell_num - 1
        if self.pos[-1,0]<0 or self.pos[-1,1]<0:
            status = False
        elif self.pos[-1,0]>boundary or self.pos[-1,1]>boundary:
            status = False
        else :
            for ind, loc in enumerate(self.get_body()):
                if not ind==self.len-1:
                    if self.pos[-1,0] == loc[0] and self.pos[-1,1] == loc[1]:
                        status = False
                        break
        return status

class game_class:
    def __init__(self):
        self.fruit = fruit_class()
        self.sneak = sneak_class()
        self.frame_counter = 0

    def start_over(self):
        self.sneak.pos = np.asarray([(5, 5), (5, 6), (5, 7)])
        self.sneak.direction = np.asarray((+1, 0))
        self.sneak.len = len(self.sneak.pos)
        # place in the middle
        self.fruit.x = int(cell_num/2)
        self.fruit.y = int(cell_num/2)

    def finish(self):
        print('EXIT SUCCESSFUL')
        pygame.quit()
        sys.exit()

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finish()

            if event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_UP    and self.sneak.direction[1]==0:  self.sneak.direction = np.asarray((0,-1))
                elif event.key == pygame.K_DOWN  and self.sneak.direction[1]==0:  self.sneak.direction = np.asarray((0,+1))
                elif event.key == pygame.K_RIGHT and self.sneak.direction[0]==0:  self.sneak.direction = np.asarray((+1,0))
                elif event.key == pygame.K_LEFT  and self.sneak.direction[0]==0:  self.sneak.direction = np.asarray((-1,0))

    def sneak_succeed_eating(self):
        if self.sneak.pos[-1, 0] == self.fruit.x and self.sneak.pos[-1, 1] == self.fruit.y:
            return True
        else:
            return False

    def update(self):
        self.frame_counter += 1
        if True : #self.frame_counter > 2: # update only every X frames.  This gives us a better key control
            self.frame_counter = 0
            if not self.sneak.is_alive():
                self.start_over()

            # did sneak eat the apple?
            if self.sneak_succeed_eating():
                self.sneak.move(eat=True)
                self.fruit.update(self.sneak.get_body())
            else:
                self.sneak.move()

    def draw(self):
        screen.fill((175, 215, 70))
        self.sneak.draw()
        self.fruit.draw()
        pygame.display.update()
        clock.tick(10)

def run_game():
    # init
    GAME = game_class()
    # run
    while True:
        GAME.control()  # user control (moving the sneak)
        GAME.update()   # update game
        GAME.draw()     # draw screen

if __name__ == '__main__':
    run_game()
