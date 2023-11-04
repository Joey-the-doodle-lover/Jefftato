import pygame

pygame.font.init()

font = pygame.font.SysFont('arial', 20, bold=False, italic=False)


def draw_health_bar(player, screen):
    x = 110
    y = 80
    w = 500
    h = 50
    x_gap = 10
    y_gap = 10

    bg_color = (255, 255, 255)
    lost_color = (100, 100, 100)
    hp_color = (255, 0, 0)
    text_color = (0, 0, 0)

    health_ratio = player.hp / player.max_hp
    background = pygame.rect.Rect(x, y, w, h)
    lost_health = pygame.rect.Rect(x + x_gap, y + y_gap, w - (x_gap * 2), h - (y_gap * 2))
    health = pygame.rect.Rect(x + x_gap, y + y_gap, (w - (x_gap * 2)) * health_ratio, h - (y_gap * 2))
    pygame.draw.rect(screen, bg_color, background)
    pygame.draw.rect(screen, lost_color, lost_health)
    pygame.draw.rect(screen, hp_color, health)

    text = font.render(f"HP: {round(player.hp, 1)} / {round(player.max_hp, 1)}", True, text_color)
    screen.blit(text, health)


def draw_stamina_bar(player, screen):
    x = 110
    y = 150
    w = 500
    h = 50
    x_gap = 10
    y_gap = 10

    bg_color = (255, 255, 255)
    lost_color = (100, 100, 100)
    stam_color = (0, 255, 0)
    text_color = (0, 0, 0)

    stamina_ratio = player.stamina / player.max_stamina
    background = pygame.rect.Rect(x, y, w, h)
    lost_stam = pygame.rect.Rect(x + x_gap, y + y_gap, w - (x_gap * 2), h - (y_gap * 2))
    stamina = pygame.rect.Rect(x + x_gap, y + y_gap, (w - (x_gap * 2)) * stamina_ratio, h - (y_gap * 2))
    pygame.draw.rect(screen, bg_color, background)
    pygame.draw.rect(screen, lost_color, lost_stam)
    pygame.draw.rect(screen, stam_color, stamina)

    text = font.render(f"Stamina: {round(player.stamina, 1)} / {round(player.max_stamina, 1)}", True, text_color)
    screen.blit(text, lost_stam)


def draw_ability_cooldowns(player, frame, screen):
    w = 50
    h = 250
    x_gap = 10
    y_gap = 10

    bg_color = (255, 255, 255)
    lost_color = (100, 100, 100)
    charging_color = (255, 128, 0)
    ready_color = (255, 0, 0)
    text_color = (0, 0, 0)

    #  woof
    woof_time_ratio = player.woof_remaining_cooldown / player.woof_cooldown_length

    woof_x = 110
    woof_y = 750

    background = pygame.rect.Rect(woof_x, woof_y, w, h)
    woof = pygame.rect.Rect(woof_x + x_gap, woof_y + y_gap, w - 2 * x_gap, h - 2 * y_gap)
    lost_woof = pygame.rect.Rect(woof_x + x_gap, woof_y + y_gap, w - 2 * x_gap, (h - 2 * y_gap) * woof_time_ratio)

    pygame.draw.rect(screen, bg_color, background)
    pygame.draw.rect(screen, charging_color, woof)
    pygame.draw.rect(screen, lost_color, lost_woof)
    if woof_time_ratio <= 0:
        pygame.draw.rect(screen, ready_color, woof)
        text = font.render(f"woof ready", True, text_color)
        screen.blit(text, woof)
    else:
        text = font.render(f"woof: {max(0, round(player.woof_remaining_cooldown, 1))} / {player.woof_cooldown_length}", True, text_color)
        screen.blit(text, woof)

    #  dash
    dash_time_ratio = player.dash_remaining_cooldown / player.dash_cooldown_length

    dash_x = 185
    dash_y = 750

    background = pygame.rect.Rect(dash_x, dash_y, w, h)
    dash = pygame.rect.Rect(dash_x + x_gap, dash_y + y_gap, w - 2 * x_gap, h - 2 * y_gap)
    lost_dash = pygame.rect.Rect(dash_x + x_gap, dash_y + y_gap, w - 2 * x_gap, (h - 2 * y_gap) * dash_time_ratio)

    pygame.draw.rect(screen, bg_color, background)
    pygame.draw.rect(screen, charging_color, dash)
    pygame.draw.rect(screen, lost_color, lost_dash)
    if dash_time_ratio <= 0:
        pygame.draw.rect(screen, ready_color, dash)
        text = font.render(f"dash ready", True, text_color)
        screen.blit(text, dash)
    else:
        text = font.render(f"dash: {max(0, round(player.dash_remaining_cooldown, 1))} / {player.dash_cooldown_length}", True, text_color)
        screen.blit(text, dash)
