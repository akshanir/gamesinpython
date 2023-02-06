import sys
import pygame
import random
import copy
from numpy import gcd

screenHeight, screenWidth = 1280, 720
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()


class Game:
    def __init__(self):
        self.boxSize = gcd(screenHeight, screenWidth) // 16
        self.N = screenHeight // self.boxSize
        self.M = screenWidth // self.boxSize
        self.surface = pygame.display.set_mode((screenHeight, screenWidth))
        self.grid = [[random.randint(0, 1) for i in range(self.M)]
                     for j in range(self.N)]
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] >= 2:
                    self.grid[i][j] = 1
                    
    def printState(self):
        for i in range(self.N):
            for j in range(self.M):
                pygame.draw.rect(self.surface, GREEN if self.grid[i][j] else BLACK, pygame.Rect(
                    self.boxSize * i, self.boxSize * j, self.boxSize, self.boxSize))
        pygame.display.flip()

    def calculateNextState(self):
        # ask about a better way for the grid
        nextGenerationGrid = [
            [0 for i in range(self.M)] for j in range(self.N)]
        for i in range(self.N):
            for j in range(self.M):
                sum = 0
                # this is really ugly but for now I guess it'll have to do
                if i > 0:
                    sum += self.grid[i-1][j]
                if j > 0:
                    sum += self.grid[i][j-1]
                if i < self.N-1:
                    sum += self.grid[i+1][j]
                if j < self.M-1:
                    sum += self.grid[i][j+1]
                if i > 0 and j > 0:
                    sum += self.grid[i-1][j-1]
                if i < self.N-1 and j < self.M-1:
                    sum += self.grid[i+1][j+1]
                if i > 0 and j < self.M-1:
                    sum += self.grid[i-1][j+1]
                if i < self.N-1 and j > 0:
                    sum += self.grid[i+1][j-1]
                ##########################################################
                if self.grid[i][j] and (sum == 2 or sum == 3) or not self.grid[i][j] and sum == 3:
                    nextGenerationGrid[i][j] = 1

        self.grid = nextGenerationGrid

    def gameloop(self):
        posX, posY = 0, 0
        while True:
            self.printState()
            self.calculateNextState()
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def start(self):
        self.gameloop()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
