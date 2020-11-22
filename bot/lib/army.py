import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units


class ArmyManager:
    def __init__(self, bot: sc2.BotAI) -> None:
        self.bot = bot

    def _get_random_enemy_building_position(self) -> Point2:
        if self.bot.enemy_structures:
            random_building: Unit = random.choice(self.bot.enemy_structures)
            return random_building.position
        return self.bot.enemy_start_locations[0]

    def manage_army(self, iteration: int):
        if iteration % 50 == 0:
            if self.bot.townhalls:
                forces: Units = self.bot.units.of_type(
                    {UnitTypeId.ZERGLING, UnitTypeId.HYDRALISK}
                )
                if self.bot.units(UnitTypeId.HYDRALISK).amount >= 10:
                    for unit in forces.idle:
                        unit.attack(self._get_random_enemy_building_position())
            else:
                self._final_assault()

    def _final_assault(self):
        """If all our townhalls are dead, send all our units to attack"""
        for unit in self.bot.units.of_type(
            {
                UnitTypeId.DRONE,
                UnitTypeId.QUEEN,
                UnitTypeId.ZERGLING,
                UnitTypeId.HYDRALISK,
            }
        ):
            unit.attack(self.bot.enemy_start_locations[0])
