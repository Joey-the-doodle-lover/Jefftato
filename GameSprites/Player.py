import math
import pygame
import random

from FrameContext import FrameContext
from GameSprites.PlayerAttacks import PlayerAttacks
from GameSprites.Weapons import Weapons
from ParentSpites.animation import ImageLoader, Animation
from ParentSpites.GameSprite import GameSprite
from RandomFunctions import locate_element, mean_list, replace_element


class Player(GameSprite):
    """
    the following are the stats of the player
    it is currently incomplete, so more will be added as needed
    most of these haven't been implimented yet:
    lacks kibble stat
    lacks xp stats
    lacks boss damage increase, along with a boss enemy to apply it to
    lacks fire
    lacks luck, or anything to apply it to
    lacks consumable stats, or treats to apply it to
    """
    # xp stats
    xp = 0  # a subunit of a level. collect enough xp to level up
    xp_gain = 0  # % percent increase in xp gained
    level = 1  # these provide stat improvements

    # health and stamina
    max_hp = 50  # max hp is the cap on player life
    hp = max_hp  # hp is the hitpoints a player has until they die
    max_stamina = 100  # the maximum stamina of the player
    stamina = max_stamina  # stamina is a stat that feuls special abilitys

    # kibble, the currancy of jefftato
    kibble = 0  # the currancy of the game
    sharking = 0  # kibble gained at the end of each round
    double_kibble_chance = 0  # % chance to get 2 kibble instead of 1
    kibble_heal_chance = 0  # % chance to heal when picking up kibble
    pick_up_range = 0  # % increase to distance kibble is attracted to you from
    treet_box_value = 0  # number of kibble earned from a treat box
    shop_price = 0  # % increase in shop prices
    free_rerolls = 0  # number of free rerolls granted in the shop each wave

    # abilitys
    woof_remaining_cooldown = 0  # time remaining on the cooldown of a woof in seconds
    woof_cooldown_length = 10  # length of cooldown on a woof in seconds
    dash_remaining_cooldown = 0  # time remaining on the cooldown of a dash in seconds
    dash_cooldown_length = 3  # length of cooldown on a dash in seconds
    dash_time = 0  # time remaining on a dash in seconds
    dash_duration = 0.25  # the number of seconds a dash lasts

    # immunity
    next_hittable = 0  # number of seconds until player can be hit by enemy again
    immunity_duration = 0.5  # immunity frame duration after being hit by an enemy

    # hp related modifiers
    hp_regeneration = 1  # amount of hp regenerated passsivly per second
    life_steal = 20  # bonus percentant chance on a weapon to heal 1 hp on hit
    armor = 20  # reduces percent damage the player takes by 1 / (1 + (x / 15))
    dodge = 30  # % chance to dodge an attack
    dodge_cap = 90  # maximum dodge chance

    # stamina related modifiers
    stamina_regeneration = 5  # amount of stamina recovered passivly per second

    # damage related modifiers
    damage = 100  # % increase in damage
    attack_speed = 0  # % increase in attack speed
    crit_chance = 25  # % increase in dealing double damage
    melee_damage = 10  # deal x bonus damage on melee weapons
    ranged_damage = 60  # deal x bonus damage on ranged weapons
    elemental_damage = 20  # deal x bonus damage on elemental weapons
    engineering = 20  # deal x bonus damage on engineering weapons
    boss_damage = 0  # % increase in damage to boss type enemys

    # projectile modifiers
    extra_range = 200  # extra centimeters traveled by a projectile
    bounces = 0  # number of times a projectile will bounce off of a target
    peircing = 0  # number of times a projectile will go through a target
    peircing_damage = 0  # % increase in damage after each pierce

    # movement
    base_speed = 5  # mps of movement
    speed = 50  # % speed increase

    # explosions:
    explosion_damage = 0  # % increase to the explosive power an explosion
    explosion_size = 0  # % increase to the size of an explosion
    force_explosion = False  # will make a bullet projectile always explode

    # fire
    burn_speed = 0  # the speed fire applys damage
    burn_spread = 0  # the number of times a fire can spread

    knockback = 0  # pushes the enemys this many centimeters based on where they were hit
    luck = 0  # will impact a variety of things in game, from item rarity, to treat chance, and more.
    consumable_heal = 0  # bonus health gained from treats

    """
    the following are the weapons of the player
    """

    gun = Weapons(("gun", "basic"), 5, 0, 1, 0, 0, 0.5, 5, 1, 250, 1, 0, -50, 0, 100, 1, 0, 1, False)
    fast_gun = Weapons(("gun"), 3, 0, 1, 0, 0, 0.25, 5, 1, 500, 1, 0, -50, 0, 25, 0, 0, 1, False)
    medical_gun = Weapons(("gun", "medical"), 0, 0, 0, 0, 0, 1, 0, 0, 500, 1, 0, 0, 0, 0, 0, 50, 5, False)

    infinity_gun = Weapons(("gun", "debug"), 1e7, 5, 5, 5, 5, 1 / 60, 100, 0, 1e5, 0, 5, 0, 0, 0, 0, 100, 0, False)
    knockback_gun = Weapons(("gun", "joke", "debug"), 0, 0, 0, 0, 0, 0.5, 0, 0, 250, 1, 0, -100, 5, 500, 10, 0, 0,
                            False)
    bounce_test = Weapons(("gun", "test"), 100, 0, 0, 0, 0, 0.5, 0, 0, 500, 0, 0, 0, 100, 0, 0, 0, 0, False)
    pierce_test = Weapons(("gun", "test"), 1000, 0, 0, 0, 0, 1, 0, 0, 5000, 0, 10, 0, 0, 0, 0, 0, 0, False)
    explosion_test = Weapons(("gun", "explosion", "test"), 10, 0, 1, 0, 0, 0.5, 5, 1, 500, 1, 0, -50, 0, 25, 1, 5, 1,
                             True)

    weapons = []
    time_until_next_attack = []
    weapon_location = []  # stores an array of the weapon locations
    weapon_distance = 1
    weapon_radian = 0
    weapon_spin_speed = 10  # in seconds

    for i in range(len(weapons)):
        time_until_next_attack.append(0)
        weapon_location.append([0, 0])

    # the sprite groups belonging to a player
    projectiles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    def __init__(self):
        super().__init__(dog_idle_animation)
        self.cowering = False
        self.cowering_last_frame = False

    def woof(self, enemies):
        self.animation = dog_woof_animation
        self.animation.reset()

        for enemy in enemies:
            if math.sqrt(((self.x - enemy.x) ** 2) + ((self.y - enemy.y) ** 2)) < 10:
                enemy.knockback((self.x, self.y), 10, 0.5)
                enemy.unstuned = 5

        self.stamina -= 25
        self.woof_remaining_cooldown = 10

    def blush(self):
        self.animation = dog_blush_animation
        self.animation.reset()

    def update(self, elapsed, frame_context: FrameContext, *args):
        super().update(elapsed, frame_context)
        self.player_hit_by_enemies(frame_context.enemies)

        self.set_weapon_locations()

        self.hp = min(self.max_hp, self.hp + self.hp_regeneration * elapsed)
        if not self.cowering:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regeneration * elapsed)

        if (self.animation != dog_woof_animation and self.animation != dog_blush_animation) \
                or self.animation.is_finished():
            if abs(self.vx) > 0.0 or abs(self.vy) > 0.0:
                self.animation = dog_run_animation
            else:
                self.animation = dog_cower_animation if self.cowering else dog_idle_animation

        self.update_time(elapsed)

    def update_time(self, elapsed):
        self.woof_remaining_cooldown = max(self.woof_remaining_cooldown - elapsed, 0)
        self.dash_remaining_cooldown = max(self.dash_remaining_cooldown - elapsed, 0)
        self.dash_time = max(self.dash_time - elapsed, 0)
        self.next_hittable = max(self.next_hittable - elapsed, 0)

    def controls(self, enemies, elapsed):
        angle = []

        keys_pressed = pygame.key.get_pressed()
        if not self.cowering:
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                angle.append(0.0)
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                angle.append(0.5)
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                angle.append(1.0)
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                angle.append(1.5)

        #  remove oppisite angles
        if 0.0 in angle and 1.0 in angle:
            angle.pop(locate_element(angle, 0.0)[0])
            angle.pop(locate_element(angle, 1.0)[0])
        if 0.5 in angle and 1.5 in angle:
            angle.pop(locate_element(angle, 0.5)[0])
            angle.pop(locate_element(angle, 1.5)[0])

        if 0.0 in angle and 1.5 in angle:
            angle = replace_element(angle, 0.0, 2.0)

        self.vx = 0.0
        self.vy = 0.0
        move_speed = (1.0 + (self.speed / 100.0)) * self.base_speed
        if self.dash_time > 0:
            move_speed *= 10
        pi = 3.1415926535897932384626433
        if len(angle) > 0:
            angle = mean_list(angle)
            if angle > 1:
                self.flipped = False
            elif angle < 1:
                self.flipped = True
            self.vx = move_speed * math.sin(angle * pi)
            self.vy = move_speed * math.cos(angle * pi)

        if keys_pressed[pygame.K_SPACE] and self.woof_remaining_cooldown == 0 and self.stamina >= 25:
            self.woof(enemies)
        if keys_pressed[pygame.K_l]:
            self.blush()
        if keys_pressed[pygame.K_f] and self.dash_remaining_cooldown == 0 and self.stamina >= 10:
            self.dash_time = self.dash_duration
            self.dash_remaining_cooldown = self.dash_cooldown_length
            self.next_hittable = self.dash_duration
            self.stamina -= 10

        self.cowering_last_frame = self.cowering
        self.cowering = keys_pressed[pygame.K_c] and self.stamina > (100 / (15 * 60))
        self.cower(elapsed)

    def generate_projectiles(self, elapsed, enemies):
        for i, weapon in enumerate(self.weapons):
            self.time_until_next_attack[i] -= elapsed
            while self.time_until_next_attack[i] <= 0:
                bullet = PlayerAttacks((self.weapon_location[i][0], self.weapon_location[i][1]), weapon, self)
                self.projectiles.add(bullet)
                bullet.set_direction(enemies)
                self.time_until_next_attack[i] += weapon.use_time * (1 + self.attack_speed / 100)

    def remove_bullets(self):
        for bullet in self.projectiles:
            if bullet.should_remove():
                bullet.kill()

    def set_weapon_locations(self):
        if len(self.weapons) > 0:
            tau = 6.283185307
            self.weapon_radian += 1 / (self.weapon_spin_speed * 60) * tau
            self.weapon_radian %= tau
            radian_per_weapon = tau / len(self.weapons)
            radian = self.weapon_radian
            for location in self.weapon_location:
                radian += radian_per_weapon
                location[0] = self.x + self.weapon_distance * math.cos(radian)
                location[1] = self.y + self.weapon_distance * math.sin(radian)

    def player_hit_by_enemies(self, enemies):
        for enemy in enemies:
            if enemy.harmless == 0:
                if self.next_hittable == 0:
                    if pygame.Rect.colliderect(self.rect, enemy.rect):
                        self.next_hittable += self.immunity_duration
                        if random.randint(1, 100) > min(self.dodge, self.dodge_cap):
                            self.hp -= enemy.power * (1 / (1 + (self.armor / 15)))
                else:
                    break

    def cower(self, elapsed):
        if self.cowering and not self.cowering_last_frame:
            self.armor = max(2 * (self.armor + 25), self.armor)
            self.immunity_duration *= 2
        if not self.cowering and self.cowering_last_frame:
            self.armor = min((self.armor / 2) - 25, self.armor)
            self.immunity_duration /= 2
        if self.cowering:
            self.stamina -= 5 * elapsed


image_loader = ImageLoader('assets/jeff')
dog_run_animation = Animation(image_loader.load_images('dog-run'), 0.2)
dog_idle_animation = Animation(image_loader.load_images('dog-idle'), 0.4)
dog_woof_animation = Animation(image_loader.load_images('dog-woof'), 0.25, False)
dog_blush_animation = Animation(image_loader.load_images('dog-blush'), 0.35, False)
dog_cower_animation = Animation(image_loader.load_images('dog-cower'), 0.3)
