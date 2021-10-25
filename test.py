import pygame

pygame.init()
window = pygame.display.set_mode((640, 640))

sprite1 = pygame.sprite.Sprite()
sprite1.image = pygame.Surface((80, 80), pygame.SRCALPHA)
pygame.draw.circle(sprite1.image, (255, 0, 0), (40, 40), 40)
sprite1.rect = pygame.Rect(*window.get_rect().center, 0, 0).inflate(40, 40)
sprite2 = pygame.sprite.Sprite()
sprite2.image = pygame.Surface((80, 80), pygame.SRCALPHA)
pygame.draw.circle(sprite2.image, (0, 255, 0), (40, 40), 40)
sprite2.rect = pygame.Rect(*window.get_rect().center, 0, 0).inflate(80, 80)

all_group = pygame.sprite.Group([sprite2, sprite1])
test_group = pygame.sprite.Group(sprite2)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sprite1.rect.center = pygame.mouse.get_pos()
    sprite1.rect.centerx -= 15
    sprite1.rect.centery -= 15
    collide = pygame.sprite.spritecollide(sprite1, test_group, False, pygame.sprite.collide_circle)

    window.fill(0)
    all_group.draw(window)
    for s in collide:
        pygame.draw.circle(window, (255, 255, 255), s.rect.center, s.rect.width // 2, 5)
    pygame.display.flip()

pygame.quit()
exit()