import sys, pygame


screenHeight, screenWidth = 720, 720
N = 8
boxSize = 720 // 8 
board= [[0 for i in range(N)]for i in range(N)]
surface = pygame.display.set_mode((screenHeight,screenWidth))
green = (0,255,0) 
white = (255, 255, 255)
black = (0, 0, 0)
asset = pygame.image.load("pieces.png")

def printBoard():
  for i in range(N):
    for j in range(N):
      pygame.draw.rect(surface, green, pygame.Rect(boxSize * i, boxSize * j, boxSize, boxSize))
  surface.blit(asset, (0, 0))
  pygame.display.flip()
  return
print(board)
def gameloop():  
  while 1:
    printBoard()
    pygame.time.wait(100)
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
  return
def main():
  gameloop()
  return 0
if __name__ == '__main__':
    main()
