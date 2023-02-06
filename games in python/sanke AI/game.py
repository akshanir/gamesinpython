from mimetypes import init
from random import randint, randrange
from unittest import skip
from numpy import gcd
import pygame
import sys
from Queue import Queue

screenHeight, screenWidth = 720, 720
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

class Game:

    def __init__(self) -> None:
        pygame.init()
        self.boxSize = gcd(screenHeight, screenWidth) // 30
        self.N = screenHeight // self.boxSize
        self.M = screenWidth // self.boxSize
        self.surface = pygame.display.set_mode((screenWidth, screenHeight))
        self.grid = [[0]*self.M for k in range(self.N)]
        self.oldboard = [[0]*self.M for k in range(self.N)]
        self.snake = Queue()
        self.snake.push(0, 0)
        self.headX = 0
        self.headY = 0
        self.grid[0][0] = 1
        self.generate_berry()
        self.dir = 2  # -1 1 -2 2
        self.freez = 0
        print(self.N, self.M)

    def printState(self):
        yes = True
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j]  != 2:
                    yes = False
                if self.oldboard[i][j] != self.grid[i][j]:
                    pygame.draw.rect(self.surface, white if self.grid[i][j] == 0 else green if self.grid[i][j] == 1 else red, pygame.Rect(
                    self.boxSize * j, self.boxSize * i, self.boxSize, self.boxSize))
                self.oldboard[i][j] = self.grid[i][j]
        pygame.display.flip()

    def generate_berry(self):
        if(self.N * self.M - self.snake.size() == 0):
            return
        x = randint(0, self.N * self.M - self.snake.size() - 1)
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 0:
                    if x == 0:
                        self.berryX = j
                        self.berryY = i
                        self.grid[i][j] = 2
                    x -= 1

    def change_dir(self, dir):
        if dir == -self.dir:
            return
        self.dir = dir

    def setState(self):
        if self.dir == -2:
            self.headY = (self.headY - 1 + self.N) % self.N
        elif self.dir == 2:
            self.headY = (self.headY + 1) % self.N
        elif self.dir == -1:
            self.headX = (self.headX - 1 + self.M) % self.M
        elif self.dir == 1:
            self.headX = (self.headX + 1) % self.M
        self.snake.push(self.headX, self.headY)

        if self.grid[self.headY][self.headX] != 2:
            self.grid[self.snake.front()[1]][self.snake.front()[0]] = 0
            self.snake.pop()
        else:
            self.generate_berry()
        if self.grid[self.headY][self.headX] == 1:
            self.freez = 1

        self.grid[self.headY][self.headX] = 1

    def frozen(self):
        return self.freez

    def initialize_cycle(self):
        order = self.order = [[0]*self.M for k in range(self.N)]
        N = self.N
        M = self.M
        cnt = 0
        # first column
        for i in range(N):
            order[i][0] = cnt
            cnt += 1
        # last row
        for i in range(1, M):
            order[N-1][i] = cnt
            cnt += 1
        # now the rest
        for j in range(M-1, 0, -1):
            if j % 2:
                for i in range(N-2, -1, -1):
                    order[i][j] = cnt
                    cnt += 1
            else:
                for i in range(0, N-1):
                    order[i][j] = cnt
                    cnt += 1

    def play_by_the_cycle(self):
        order = self.order
        j = self.headX
        i = self.headY
        n = self.N
        m = self.M
        mx = n * m
        if i-1 >= 0 and order[i-1][j] == (order[i][j] + 1) % mx:
            self.change_dir(-2)
        if i+1 < n and order[i+1][j] == (order[i][j] + 1) % mx:
            self.change_dir(2)
        if j-1 >= 0 and order[i][j-1] == (order[i][j] + 1) % mx:
            self.change_dir(-1)
        if j+1 < m and order[i][j+1] == (order[i][j] + 1) % mx:
            self.change_dir(1)

    def nothing_in_range(self, l, r):
        yes = True
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 0:
                    continue
                if l < r and l < self.order[i][j] and self.order[i][j] < r:
                    yes = False
                if l > r and (l < self.order[i][j] or self.order[i][j] < r):
                    yes = False
                if self.order[i][j] == r and self.grid[i][j] == 1:
                    yes = False
        return yes

    def play_with_shortcuts(self):
        order = self.order
        j = self.headX
        i = self.headY
        n = self.N
        m = self.M
        mx = n * m
        best = 0
        berry = order[self.berryY][self.berryX]
        if 1:
            skipped = (order[(i-1+n)%n][j] - order[i][j] + mx) % mx
            if self.nothing_in_range(order[i][j], order[(i-1+n)%n][j]) and self.snake.size() + 1 <= n * m - skipped:
                if skipped > best:
                    best = skipped
                    self.change_dir(-2)
        if 1:
            skipped = (order[(i+1)%n][j] - order[i][j] + mx) % mx
            if self.nothing_in_range(order[i][j], order[(i+1)%n][j]) and self.snake.size() + 1 <= n * m - skipped:
                if skipped > best:
                    best = skipped
                    self.change_dir(2)
        if 1:
            skipped = (order[i][(j-1+m)%m] - order[i][j] + mx) % mx
            if self.nothing_in_range(order[i][j], order[i][(j-1+m)%m]) and self.snake.size() + 1 <= n * m - skipped:
                if skipped > best:
                    best = skipped
                    self.change_dir(-1)
        if 1:
            skipped = (order[i][(j+1)%m] - order[i][j] + mx) % mx
            if self.nothing_in_range(order[i][j], order[i][(j+1)%m]) and self.snake.size() + 1 <= n * m - skipped:
                if skipped > best:
                    best = skipped
                    self.change_dir(1)


if __name__ == '__main__':
    game = Game()
    game.initialize_cycle()
    steps = 0
    while 1:
        if steps % 1000 == 0:
            game.printState()
        if not game.frozen():
            steps += 1
            # game.printState()
            # pygame.time.wait(50)
            game.setState()
            # now for cycle stuff
            if game.snake.size() > game.N * game.M // 2:
                game.play_by_the_cycle()
            else:
                game.play_with_shortcuts()
            # end of cycle stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(steps)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.change_dir(-2)
                if event.key == pygame.K_DOWN:
                    game.change_dir(2)
                if event.key == pygame.K_LEFT:
                    game.change_dir(-1)
                if event.key == pygame.K_RIGHT:
                    game.change_dir(1)
    