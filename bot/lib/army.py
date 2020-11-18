import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.units import Units


def get_random_enemy_building_position(bot: sc2.BotAI) -> Point2:
    if bot.enemy_structures:
        return random.choice(bot.enemy_structures).position
    return bot.enemy_start_locations[0]


def attack_base(bot: sc2.BotAI, forces: Units, timer: bool):
    if bot.units(UnitTypeId.HYDRALISK).amount >= 10 and timer:
        for unit in forces.idle:
            unit.attack(get_random_enemy_building_position(bot))


def final_assault(bot: sc2.BotAI):
    """If all our townhalls are dead, send all our units to attack"""
    for unit in bot.units.of_type(
        {
            UnitTypeId.DRONE,
            UnitTypeId.QUEEN,
            UnitTypeId.ZERGLING,
            UnitTypeId.HYDRALISK,
        }
    ):
        unit.attack(bot.enemy_start_locations[0])
