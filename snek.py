import pygame
from random import randint


pygame.init()

BACKGROUND = (100, 100, 100)
SNEK_COLOR = (200, 200, 255)
FOOD_COLOR = (255, 200, 200)
SIZE = 10
FPS = 15


class Segment:
    def __init__(self, x, y, dx=0, dy=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


class Snek:
    def __init__(self):
        self.width = 600
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game name of SNEK')
        self.snek = [Segment(0, 0, SIZE, 0)]
        self.clock = pygame.time.Clock()
        self.locate_food()


    def restart(self):
        self.snek = [Segment(0, 0, SIZE, 0)]
        self.locate_food()


    def draw(self, lost):
        if not lost:
            self.display.fill(BACKGROUND)
            for seg in self.snek:
                rect = pygame.Rect(seg.x, seg.y, SIZE, SIZE)
                pygame.draw.rect(self.display, SNEK_COLOR, rect)
            food_rect = pygame.Rect(self.food.x, self.food.y, SIZE, SIZE)
            pygame.draw.rect(self.display, FOOD_COLOR, food_rect)
            pygame.display.flip()
        else:
            self.display.fill((255, 0, 0))
            for seg in self.snek:
                rect = pygame.Rect(seg.x, seg.y, SIZE, SIZE)
                pygame.draw.rect(self.display, SNEK_COLOR, rect)
            food_rect = pygame.Rect(self.food.x, self.food.y, SIZE, SIZE)
            pygame.draw.rect(self.display, FOOD_COLOR, food_rect)
            font = pygame.font.SysFont('arial', 32, True)
            text = font.render('You Lose!', True, (255, 255, 255))
            self.display.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            self.restart()


    def move(self):
        seg = self.snek[0]
        old_x = seg.x
        old_y = seg.y
        if 0 <= seg.x + seg.dx <= self.width - SIZE:
            seg.x += seg.dx
        if 0 <= seg.y + seg.dy <= self.height - SIZE:
            seg.y += seg.dy
        for i in range(1, len(self.snek)):
            next_x = self.snek[i].x
            next_y = self.snek[i].y
            self.snek[i].x = old_x
            self.snek[i].y = old_y
            old_x = next_x
            old_y = next_y
            # Check for collision
            if self.snek[i].x == seg.x and self.snek[i].y == seg.y:
                return True

        head = pygame.Rect(seg.x, seg.y, SIZE, SIZE)
        if head.colliderect(self.food):
            self.locate_food()
            self.eat_food()

        return False


    def locate_food(self):
        x = randint(0, (self.width - SIZE) // SIZE) * SIZE
        y = randint(0, (self.height - SIZE) // SIZE) * SIZE
        self.food = pygame.Rect(x, y, SIZE, SIZE)

    
    def eat_food(self):
        x = self.snek[-1].x - self.snek[-1].dx
        y = self.snek[-1].y - self.snek[-1].dy
        self.snek.append(Segment(x, y))
    
    
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    # Don't allow reversing
                    head = self.snek[0]
                    if event.key == pygame.K_RIGHT and head.dx == 0:
                        head.dx = SIZE
                        head.dy = 0
                    if event.key == pygame.K_LEFT and head.dx == 0:
                        head.dx = -SIZE
                        head.dy = 0
                    if event.key == pygame.K_UP and head.dy == 0:
                        head.dx = 0
                        head.dy = -SIZE
                    if event.key == pygame.K_DOWN and head.dy == 0:
                        head.dx = 0
                        head.dy = SIZE

            lost = self.move()
            self.draw(lost)
            self.clock.tick(FPS)


if __name__ == '__main__':
    snek = Snek()
    snek.run_game()