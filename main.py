import pygame

pygame.init()

import random

screen_height = 1080
screen_width = 1920
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60


class Game:
    def __init__(self, camera_x, camera_y, map_width, map_height, wave):
        self.cameraX = camera_x
        self.cameraY = camera_y
        self.map_width = map_width
        self.map_height = map_height
        self.wave = wave

    class Enemy:
        def __init__(self, x, y, vx, vy, hp, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.hp = hp
            self.type = typ

    class PlayerAttacks:
        def __init__(self, x, y, vx, vy, dmg, rang, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.dmg = dmg
            self.range = rang
            self.type = typ

    class EnemyAttacks:
        def __init__(self, x, y, vx, vy, dmg, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.dmg = dmg
            self.type = typ

    class Structures:
        def __init__(self, x, y, typ):
            self.x = x
            self.y = y
            self.type = typ

    class Consumables:
        def __init__(self, x, y, value, typ):
            self.x = x
            self.y = y
            self.value = value
            self.type = typ


class Player:
    """
    hp = health, reg = regeneration, ls = life steal, dmg = damage, mdmg = melee damage, rdmg = ranged damage,
    edmg = elemental damage, a_s = attack speed, crit = crit chance, eng =  engineering, rng = range,
    amr = armor, dg = dodge, spd = speed, lk = luck, harv = harvesting, con_heal consumable heal,
    mhc = material heal chance, xp_g xp gain, pr = pickup range, price = item price, ex_dmg explosion damage,
    ex_size = explosion size, bonc = projectile bounces, prc = projectile peircing, prc_dmg = peircing damage,
    boss = damage agaist bosses, brn_spd = burning speed, brn_sprd = burning spread, kb = knockback,
    dmc = double material chance, trt_bx = materials from treat box, f_rll = free rerolls, tree = tree quanity,
    enm = enemy quanity, enm_spd = enemy speed.
    """

    def __init__(self, x, y, vx, vy, xp, lv, hp, reg, ls, dmg, mdmg, rdmg, edmg, a_s, crit, eng, rng, amr, dg, spd, lk,
                 harv, con_heal, mhc, xp_g, pr, price, ex_dmg, ex_size, bonc, prc, prc_dmg, boss, brn_spd, brn_sprd,
                 kb, dmv, trt_bx, f_rll, tree, enm, enm_spd):
        self.x = x
        self.y = y
        self.velocityX = vx
        self.velocityY = vy
        self.xp = xp
        self.lv = lv
        self.hp = hp
        self.regeneration = reg
        self.life_steal = ls
        self.damage = dmg
        self.melee_damage = mdmg
        self.ranged_damage = rdmg
        self.elemental_damage = edmg
        self.attack_speed = a_s
        self.crit_chance = crit
        self.engineering = eng
        self.range = rng
        self.armor = amr
        self.dodge = dg
        self.speed = spd
        self.luck = lk
        self.harvesting = harv
        self.consumable_heal = con_heal
        self.material_heal_chance = mhc
        self.xp_gain = xp_g
        self.pick_up_range = pr
        self.shop_price = price
        self.explosion_damage = ex_dmg
        self.explosion_size = ex_size
        self.bounces = bonc
        self.peircing = prc
        self.peircing_damage = prc_dmg
        self.boss_damage = boss
        self.burn_speed = brn_spd
        self.burn_spread = brn_sprd
        self.knockback = kb
        self.double_material_chance = dmv
        self.treet_box_value = trt_bx
        self.free_rerolls = f_rll
        self.tree_quanity = tree
        self.enemy_quanity = enm
        self.enemy_speed = enm_spd


game = Game(0, 0, 5000, 5000, 1)
while True:
    pygame.display.flip()
    clock.tick(fps)
