
class Weapons:
    def __init__(self, types, damage, bonus_from_melee, bonus_from_range, bonus_from_element, bonus_from_engin,
                 use_time, crit_chance, crit_chance_mod, base_range, range_modifier, pierce, pierce_damage, bounces,
                 knockback, knockback_modifier, life_steal, life_steal_modifier):
        self.types = types  # tuple of the types. ex: (gun, explosion)
        self.damage = damage
        self.bonus_from_melee = bonus_from_melee  # multiplys this by the players melee damage and adds to damage
        self.bonus_from_range = bonus_from_range  # multiplys this by the players ranged damage and adds to damage
        self.bonus_from_element = bonus_from_element  # multiplys this by the player elemental damage and adds to damage
        self.bonus_from_engin = bonus_from_engin  # multiplys this by the players engin and adds to damage
        self.use_time = use_time  # in seconds
        self.crit_chance = crit_chance
        self.crit_chance_modifier = crit_chance_mod
        self.range = base_range
        self.range_modifier = range_modifier
        self.pierce = pierce
        self.pierce_damage = pierce_damage  # multiplier on bullet damage after pierce.
        self.bounces = bounces
        self.knockback = knockback  # in cm
        self.knockback_modifier = knockback_modifier
        self.life_steal = life_steal  # % chance to heal 1 on hit
        self.life_steal_modifier = life_steal_modifier
