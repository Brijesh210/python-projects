import pygame
import const


class Sprite:

    def __init__(self, texture, xy=(0, 0)):
        self.img = pygame.image.load(texture)
        self.rect = self.img.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]
        self.speed = [0, 0]
        self.direction = [0, 0]

    def move(self):
        self.rect.move_ip(self.speed[0] * self.direction[0], self.speed[1] * self.direction[1])

    def render(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))


class Player(Sprite):
    missile_speed = 1
    fire_delay = 0
    score = 0

    def __init__(self, speed=0.5, hp=20):
        super().__init__(const.player_ship)
        self.rect.x = 1
        self.rect.y = const.SIZE_Y - self.img.get_height()
        self.speed = [speed, speed]
        self.missiles = []
        self.hp = hp

    def update(self):
        if self.hp <= 0:
            return False
        Player.fire_delay -= 1
        self.move()
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > const.SIZE_X - self.img.get_width():
            self.rect.x = const.SIZE_X - self.img.get_width()
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > const.SIZE_Y - self.img.get_width():
            self.rect.y = const.SIZE_Y - self.img.get_width()
        self.missiles[:] = [mis for mis in self.missiles if mis.update()]
        return True

    def render(self, screen):
        super().render(screen)
        for mis in self.missiles:
            mis.render(screen)

    def shoot(self):
        if Player.fire_delay <= 0:
            self.missiles.append(Missile([self.rect.x + self.img.get_width() / 2, self.rect.y]))
            Player.fire_delay = const.player_fire_delay

    def take_damage(self):
        self.hp -= 1


class Missile(Sprite):
    speed = 2

    def __init__(self, xy):
        super().__init__(const.missile, xy)
        self.object = pygame.image.load(const.missile)
        self.rect.x = self.rect.x - self.object.get_width() / 2
        self.speed = [0, Missile.speed]
        self.direction = [0, -1]

    def update(self):
        if self.rect.y < 0:
            return False
        self.move()
        return True


class Ufo(Sprite):
    speed = 1

    def __init__(self, xy, expls, hp=1):
        super().__init__(const.ufo_one, xy)
        self.rect.height = self.rect.height*2
        self.rect.width = self.rect.width*2
        self.img = pygame.transform.scale(self.img, (self.rect.width,self.rect.height))
        self.speed = [0, Ufo.speed]
        self.direction = [0, 1]
        self.move_delay = 5
        self.alive = True
        self.hp = hp
        k = 128
        self.explosion_frames = []
        for j in range(0, 1024, k):
            for i in range(0, 1024, k):
                self.explosion_frames.append(expls.subsurface(i, j, k, k))

    def update(self):
        if self.rect.y > const.SIZE_Y:
            return False
        elif not self.alive and len(self.explosion_frames) <= 0:
            Player.score += 1
            return False
        if self.move_delay <= 0:
            self.move()
            self.move_delay = 5
        else:
            self.move_delay -= 1
        return True

    def render(self, screen):
        if self.alive:
            super().render(screen)
        else:
            screen.blit(self.explosion_frames.pop(0), (self.rect.x - 35, self.rect.y-35))

    def collide_bullets(self, missiles):
        i = len(missiles)
        missiles[:] = [mis for mis in missiles if not mis.rect.colliderect(self.rect) == 1]
        if not i == len(missiles):
            if self.hp > 0:
                self.hp -= 1
            else:
                self.alive = False

    def collide_player(self, player):
        if self.rect.colliderect(player.rect) == 1 and self.alive:
            self.alive = False
            player.take_damage()
