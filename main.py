import sys

import pygame, math, random

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 620
screen = pygame.display.set_mode((width, height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect((x, y), (32, 32))
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)

class Thingy(pygame.sprite.Sprite):
    def __init__(self, x, y, att, defe, minsped, spawner):
        super().__init__()
        self.rect = pygame.Rect((x, y), (32, 32))
        self.image = pygame.Surface((32, 32))
        self.image.fill(spawner.team)
        self.hp = defe
        self.att = att
        self.minsped = minsped
        self.eneegy = 1
        self.spawner = spawner

    def attack(self, enemy):
        if self.eneegy > 0 and math.dist((self.rect.centerx, self.rect.centery), (enemy.rect.centerx, enemy.rect.centery)) <= 32:
            enemy.hp -= 1
            self.eneegy -= 1
            self.cooldown = 10
            if enemy.hp == 0:
                enemy.kill()

    def truup(self, block_group, echar_group):
        self.cooldown -= 1
        if self.eneegy <= 2:
            self.eneegy += 1
        keys = pygame.sprite.spritecollide(self, block_group, False)
        for e in keys:
            num = random.randint(1, 4)
            if num == 1:
                self.move_up()
            elif num == 2:
                self.move_left()
            elif num == 3:
                self.move_right()
            else:
                self.move_down()

        keys = pygame.sprite.spritecollide(self, echar_group, False)
        for e in keys:
            num = random.randint(1, 4)
            if num == 1:
                self.move_up()
            elif num == 2:
                self.move_left()
            elif num == 3:
                self.move_right()
            else:
                self.move_down()

    def move_up(self):
        self.rect.y -= 32

    def move_left(self):
        self.rect.x -= 32

    def move_right(self):
        self.rect.x += 32

    def move_down(self):
        self.rect.y += 32

    def mine(self, block):
        if self.eneegy > 0 and math.dist((self.rect.centerx, self.rect.centery),(block.rect.centerx, block.rect.centery)) <= 16:
            block.kill()
            self.spawner.eneegy += 1
            self.eneegy -= 1



class Spawner(pygame.sprite.Sprite):
    def __init__(self, x, y, team):
        super().__init__()
        self.rect = pygame.Rect((x, y), (64, 32))
        self.image = pygame.Surface((64, 32))
        self.image.fill(team)
        self.eneegy = 0
        self.team = team

    def update(self, char_groupb, char_groupr):
        if self.team == (255, 0, 0):
            pass
        else:
            self.spawn_att(char_groupb)

    def spawn_att(self, char_group):
        if self.eneegy > 0:
            new_char = Att(self.rect.x, self.rect.y, self)
            char_group.add(new_char)
            self.eneegy -= 1

    def spawn_def(self, char_group):
        if self.eneegy > 0:
            new_char = Def(self.rect.x, self.rect.y, self)
            char_group.add(new_char)
            self.eneegy -= 1

    def spawn_min(self, char_group):
        if self.eneegy > 0:
            new_char = Min(self.rect.x, self.rect.y, self)
            char_group.add(new_char)
            self.eneegy -= 1

class Att(Thingy):
    def __init__(self, x, y, spawner):
        super().__init__(x, y, 50, 10, 10, spawner)
    def update(self, block_group, echar_group):
        self.truup(block_group, echar_group)


class Def(Thingy):
    def __init__(self, x, y, spawner):
        super().__init__(x, y, 10, 50, 10, spawner)
    def update(self, block_group, echar_group):
        self.truup(block_group, echar_group)


class Min(Thingy):
    def __init__(self, x, y, spawner):
        super().__init__(x, y, 10, 10, 50, spawner)
    def update(self, block_group, echar_group):
        self.truup(block_group, echar_group)

def main():
    # Game loop.
    block_group = pygame.sprite.Group()
    spawner_group = pygame.sprite.Group()
    char_groupb = pygame.sprite.Group()
    char_groupr = pygame.sprite.Group()
    spawner1 = Spawner(width - 128, height - 128 - 16, (0, 0, 255))
    spawner2 = Spawner(width - 128, height - 192 - 16, (0, 0, 255))
    spawner3 = Spawner(64, 64, (255, 0, 0))
    spawner4 = Spawner(64, 128 , (255, 0, 0))
    spawner_group.add(spawner1)
    spawner_group.add(spawner2)
    spawner_group.add(spawner3)
    spawner_group.add(spawner4)
    for i in range(0, width, 32):
        for j in range(0, height, 32):
            if random.randint(1, 25) == 1:
                new_block = Block(i, j)
                block_group.add(new_block)
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        spawner_group.update(char_groupb, char_groupr)
        char_groupb.update(block_group, char_groupr)
        char_groupr.update(block_group, char_groupb)

        block_group.draw(screen)
        spawner_group.draw(screen)
        char_groupr.draw(screen)
        char_groupb.draw(screen)

        pygame.display.flip()
        fpsClock.tick(fps)

main()
