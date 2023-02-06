import enum
from multiprocessing import Condition
from pickle import TRUE
import sys, pygame, random, copy
from tkinter.messagebox import NO
from numpy import gcd

class Node:
   def __init__(self, X, Y, next):
      self.X = X
      self.Y = Y
      self.next = next

def main():
    # Initializing Pygame
    pygame.init()
    # Initialing Colors
    red = (255, 0, 0)
    green = (0,255,0) 
    white = (255, 255, 255)
    blue = (0, 0, 255)
    # Initializing surface
    screenHeight, screenWidth = 720, 1280
    boxSize = gcd(1280, 720) // 2
    N, M = screenHeight // boxSize, screenWidth // boxSize
    surface = pygame.display.set_mode((screenWidth,screenHeight))
    global grid
    grid = [[0 for i in range(M)] for j in range(N)]
    grid = [[0]*M for j in range(N)]
    global Y
    global X
    print(N, M)
    Y, X = random.randint(0, N-1), random.randint(0, M-1)
    global dir
    dir = 1 # 1 up 2 down 3 left 4 right
    def printState():
        for i in range(N):
            for j in range(M):
                pygame.draw.rect(surface, green if grid[i][j] else white, pygame.Rect(boxSize * j, boxSize * i, boxSize, boxSize))
        node = SnakeHead
        while node != None:
            pygame.draw.rect(surface, green, pygame.Rect(boxSize * node.X, boxSize * node.Y, boxSize, boxSize))
            node = node.next
        global eatenCounter
        pygame.draw.rect(surface, blue if eatenCounter % 5 == 0 else red, pygame.Rect(boxSize * strawBerryX, boxSize * strawBerryY, boxSize, boxSize))
        # font = pygame.font.Font(pygame.font.get_default_font(), 36)
        # # now print the text
        # text_surface = font.render('Hello world', antialias=True, color=(0, 0, 0))
        # surface.blit(text_surface, dest=(0,0))
        pygame.display.flip()
        return
    def setState():
        global Y
        global X
        if dir == 1:
            Y = (Y - 1 + N) % N
        if dir == 2:
            Y = (Y + 1) % N
        if dir == 3:
            X = (X - 1 + M) % M
        if dir == 4:
            X = (X + 1) % M
        global SnakeHead
        global strawBerryX
        global strawBerryY
        NewHead = Node(X, Y, SnakeHead)
        exists = False
        node = SnakeHead
        while node != None:
            if node.X == NewHead.X and node.Y == NewHead.Y:
                exists = True
            node = node.next
        if exists:
            global FREEZE
            FREEZE = 1
            return
        SnakeHead = NewHead
        if SnakeHead.X == strawBerryX and SnakeHead.Y == strawBerryY:
            generateStrawberry()
        else:
            node = SnakeHead
            while node.next.next != None:
                node = node.next
            node.next = None
            
        return
    def generateStrawberry():
        global eatenCounter
        eatenCounter += 1
        newStrawberryLocation = random.randint(1, freesquares)
        cnt = 0
        for i in range(N):
            for j in range(M):
                exists = False
                node = SnakeHead
                while node != None:
                    if node.X == j and node.Y == i:
                        exists = True
                    node = node.next
                if not exists:
                    cnt += 1
                if cnt == newStrawberryLocation:
                    global strawBerryX
                    global strawBerryY
                    strawBerryX = j
                    strawBerryY = i
                    return
        return
    global SnakeHead
    SnakeHead = Node(Y, X, None)
    SnakeTail = SnakeHead
    global strawBerryX
    global strawBerryY
    global freeSquares
    freesquares = N * M - 1
    global eatenCounter
    eatenCounter = -1
    generateStrawberry()
    global FREEZE
    FREEZE = False
    while 1:
        if FREEZE == 0:
            setState()
        printState()
        print(eatenCounter)
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dir != 2:
                   dir = 1
                if event.key == pygame.K_DOWN and dir != 1:
                   dir = 2
                if event.key == pygame.K_LEFT and dir != 4:
                   dir = 3
                if event.key == pygame.K_RIGHT and dir != 3:
                   dir = 4     
    return
    
if __name__ == '__main__':
    main()
