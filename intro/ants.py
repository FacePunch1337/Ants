import pygame
import random
import math

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ANT_WORKER_COLOR = (104,62,61)
ANT_SOLIDER_COLOR = (104,62,61)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 800, 600

class Shelter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_count = 0

    def receive_food(self):
        self.food_count += 1

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BaseStrategy:
    def move(self, bot, other_bots):
        pass

class WorkerStrategy(BaseStrategy):
    def move(self, bot, other_bots):
        if bot.state == "search":
            bot.search_for_food()
        elif bot.state == "deliver":
            bot.deliver_food()

class SoldierStrategy(BaseStrategy):
    def __init__(self):
        self.patrol_target = None

    def move(self, bot, other_bots):
        if bot.state == "patrol":
            if self.patrol_target is None or random.random() < 0.02:
                self.set_patrol_target(bot)
            bot.target = self.patrol_target
            bot.move_towards_target()

    def set_patrol_target(self, bot):
       
        self.patrol_target = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

   

    


class Bot:
    def __init__(self, x, y, shelter, strategy):
        self.x = x
        self.y = y
        self.state = "search"
        self.target = None
        self.food = None
        self.shelter = shelter
        self.delivered_food_count = 0
        self.returning_to_shelter = False
        self.strategy = strategy

    def render(self):
        if isinstance(self.strategy, SoldierStrategy):
            pygame.draw.circle(screen, ANT_SOLIDER_COLOR, (int(self.x), int(self.y)), 15)  # Больший круг для солдат
        else:
            pygame.draw.circle(screen, ANT_WORKER_COLOR, (int(self.x), int(self.y)), 10)

        if self.food is not None:
            pygame.draw.circle(screen, RED, (int(self.food.x), int(self.food.y)), 5)

    def move_towards_target(self):
        if self.target is not None:
            angle = math.atan2(self.target[1] - self.y, self.target[0] - self.x)
            speed = 1
            self.x += speed * math.cos(angle)
            self.y += speed * math.sin(angle)

           
        
            distance = math.sqrt((self.x - self.target[0]) ** 2 + (self.y - self.target[1]) ** 2)
            if distance < speed:
                if self.state == "search":
                    self.state = "deliver"
                    self.target = self.shelter.x, self.shelter.y
                elif self.state == "deliver":
                    self.food.x = self.x
                    self.food.y = self.y

                    if self.target == (self.shelter.x, self.shelter.y):
                        self.shelter.receive_food()
                        self.food = None
                        self.state = "search"
                        self.target = None
                        self.delivered_food_count += 1
                        self.returning_to_shelter = False
                    else:
                        self.returning_to_shelter = True

    def update(self, other_bots):
        self.strategy.move(self, other_bots)
      
        self.move_towards_target()

   
    

    def find_nearest_food(self, other_bots):
        foods = [Food(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]
        if self.food is None:
            distances = [(food, math.sqrt((self.x - food.x) ** 4 + (self.y - food.y) ** 4)) for food in foods]
            distances.sort(key=lambda x: x[1])
            for food, _ in distances:
                if all(bot.food != food for bot in other_bots):
                    self.food = food
                    self.target = food.x, food.y
                    break

    def search_for_food(self):
        self.find_nearest_food([bot for bot in bots if bot != self])
        if self.target is not None:
            self.move_towards_target()

    def deliver_food(self):
        self.move_towards_target()
        if self.food is not None and not self.returning_to_shelter:
            self.food.x = self.x
            self.food.y = self.y

   
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Game")


shelter = Shelter(WIDTH // 2, HEIGHT // 2)


bot1 = Bot(WIDTH // 2, HEIGHT // 2, shelter, WorkerStrategy())

bot2 = Bot(WIDTH // 2, HEIGHT // 2, shelter, WorkerStrategy())

bot3 = Bot(WIDTH // 2, HEIGHT // 2, shelter, WorkerStrategy())

bot4 = Bot(WIDTH // 2, HEIGHT // 2, shelter, WorkerStrategy())

bot5 = Bot(WIDTH // 2, HEIGHT // 2, shelter, SoldierStrategy())
bot5.state = "patrol"

bot6 = Bot(WIDTH // 2, HEIGHT // 2, shelter, SoldierStrategy())
bot6.state = "patrol"

bots = [bot1, bot2, bot3, bot4, bot5, bot6]

# Основной цикл
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
        

    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (shelter.x - 20, shelter.y - 20, 40, 40))

    for bot in bots:
        bot.update(bots)
        bot.render()

    font = pygame.font.Font(None, 36)
    text = font.render(f"Delivered: {shelter.food_count}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    clock.tick(60)
