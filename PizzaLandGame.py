import random
import sys

import pygame

score = 0
level = 0
misses = 0


class Player(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.sprite = pygame.image.load("assets/canvas.png")

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 30, self.y + 10, 30, 30)

    def movement(self):
        keys = pygame.key.get_pressed()
        # Goingleft
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.x - self.vel > 30:
            self.x -= self.vel

            # Goingright
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.x + self.vel < 470:
            self.x += self.vel


class Projectile(object):
    def __init__(self, y, width, height, vel, value):
        self.x = random.randint(50, 450)
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.value = value
        self.sprite = pygame.image.load("assets/pizza.png")

    def move(self):
        self.y += self.vel

    def draw(self, win):
        self.move()
        self.hitbox = (self.x + 15, self.y + 10, 30, 30)
        win.blit(self.sprite, (self.x, self.y))

    def relocate(self):
        global misses
        if self.y > 500:
            self.y = 0
            if not isbomb:
                misses += 1
            self.bomb()
            self.x = random.randint(50, 450)

    def hit(self, player):
        global score
        if self.y - self.width < player.hitbox[1] + player.hitbox[3] and self.y + self.width > player.hitbox[1]:
            if self.x + self.width > player.hitbox[0] and self.x - self.width < player.hitbox[0]:
                score += self.value
                self.x = random.randint(50, 450)
                self.y = 0
                self.bomb()

    def bomb(self):
        global isbomb
        bomber = random.randint(0, 10)
        if bomber == 10:
            self.value = -10
            self.sprite = pygame.image.load("assets/bomb.png")
            isbomb = True
        else:
            isbomb = False
            self.value = 1
            self.sprite = pygame.image.load("assets/pizza.png")


maxLevel = 0
maxScore = 0
start = True
game = False
bg = pygame.image.load("assets/start.png")
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
levelUpLim = 20


def redrawGameWindow(font, bg, man, pizza):
    levels = font.render("Level: " + str(level), 1, (40, 40, 255))
    scoreCount = font.render('Score: ' + str(score), 1, (0, 255, 0))
    missed = font.render("Misses: " + str(misses), 1, (125, 0, 0))
    win.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    win.blit(levels, (190, 30))
    win.blit(scoreCount, (30, 30))
    win.blit(missed, (330, 30))
    pizza.draw(win)
    man.draw(win)


counter = 0
autoSaveC = 0
bigpizza = pygame.image.load("assets/bigpizza.png")
counter1 = 0
startPizzaX = 100
startPizzaY = 100
yCount = 0
pizzaXMOVE = 0
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("PizzaLand")
run = False
font = pygame.font.SysFont("comicsans", 36, True)
if start:  # Startscreen
    while start:
        win.fill((0, 0, 0))
        counter += 1
        win.blit(bg, (0, 0))
        yCount += 1
        if yCount <= 40:
            startPizzaY += 1
        else:
            startPizzaY -= 1

        if yCount == 80:
            yCount = 0
        win.blit(bigpizza, (startPizzaX, startPizzaY))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            counter = 0
            while counter < 50:
                pygame.event.get()
                startPizzaX += 17
                clock.tick(60)
                counter += 1
                win.blit(bg, (0, 0))
                win.blit(bigpizza, (startPizzaX, startPizzaY))
                pygame.display.update()
                start = False
                run = True
        pygame.display.update()

pizza = Projectile(0, 96, 96, 3, 1)
man = Player(30, 330, 96, 96, 5)
bg = pygame.image.load("assets/bg.jpg")
pizza.bomb()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pizza.vel = level + 4
    redrawGameWindow(font, bg, man, pizza)
    if score >= levelUpLim:
        level += 1
        levelUpLim += 20
    if misses == 5:
        level = 0
        misses = 0
        score = 0

    man.vel = pizza.vel
    maxLevel = level
    if score > maxScore:
        maxScore = score
    pizza.relocate()
    pizza.hit(man)
    man.movement()
    clock.tick(60)
    autoSaveC += 1
    pygame.display.update()
