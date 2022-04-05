import space
import pygame
import const
import random

SIZE_X = const.SIZE_X
SIZE_Y = const.SIZE_Y

ufos = []
spawn_rate = 300  # greater is slower
hp = 20
expls = pygame.transform.scale(pygame.image.load(const.explosions),(1024,1024))


def spawn_enemies():
    global spawn_rate, ufos
    if random.randint(0, spawn_rate) == random.randint(0, spawn_rate):
        ufos.append(space.Ufo([random.randint(0, const.SIZE_X-pygame.image.load(const.ufo_one).get_width()), 0], expls, random.randint(1, 5)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
    pygame.display.set_caption("Spaceshooter")
    icon = pygame.image.load(const.icon)
    pygame.font.init()
    font = pygame.font.SysFont(const.font, 30)
    gameover_text = font.render("GAME OVER", False, (255, 50, 0))
    pygame.display.set_icon(icon)
    background = pygame.image.load(const.background)
    player = space.Player(1, hp)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.direction = [1, 0]
                if event.key == pygame.K_LEFT:
                    player.direction = [-1, 0]
                if event.key == pygame.K_UP:
                    player.direction = [0, -1]
                if event.key == pygame.K_DOWN:
                    player.direction = [0, 1]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.direction == [-1, 0]:
                    player.direction = [0, 0]
                if event.key == pygame.K_RIGHT and player.direction == [1, 0]:
                    player.direction = [0, 0]
                if event.key == pygame.K_UP and player.direction == [0, -1]:
                    player.direction = [0, 0]
                if event.key == pygame.K_DOWN and player.direction == [0, 1]:
                    player.direction = [0, 0]
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player.shoot()
        alive = player.update()
        if not alive:
            screen.blit(gameover_text, (const.SIZE_X/2-gameover_text.get_width()/2, const.SIZE_Y/2-gameover_text.get_height()/2))
        else:
            spawn_enemies()
            ufos[:] = [ufo for ufo in ufos if ufo.update()]
            screen.blit(pygame.transform.scale(background, (SIZE_X, SIZE_Y)), (0, 0))
            player.render(screen)
            screen.blit(font.render("HP " + str(player.hp), False, (255, 0, 0)), (20, 20))
            screen.blit(font.render("SCORE " + str(space.Player.score), False, (255, 0, 0)), (20, 50))

            for ufo in ufos:
                ufo.render(screen)
                ufo.collide_player(player)
                ufo.collide_bullets(player.missiles)

        pygame.display.update()


if __name__ == "__main__":
    main()
