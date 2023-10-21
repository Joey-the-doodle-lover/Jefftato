import pygame


def draw_health_bar(player, screen):
    health_ratio = player.hp / player.max_hp
    background = pygame.rect.Rect(110, 80, 450, 50)
    lost_health = pygame.rect.Rect(120, 90, 430, 30)
    health = pygame.rect.Rect(120, 90, 430 * health_ratio, 30)
    pygame.draw.rect(screen, (255, 255, 255), background)
    pygame.draw.rect(screen, (100, 100, 100), lost_health)
    pygame.draw.rect(screen, (255, 0, 0), health)
