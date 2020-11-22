import sc2
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit


class QueenManager:
    def __init__(self, bot: sc2.BotAI) -> None:
        self.bot = bot

    def manage_queens(self, hq: Unit):
        for queen in self.bot.units(UnitTypeId.QUEEN).idle:
            if queen.energy >= 25:
                queen(AbilityId.EFFECT_INJECTLARVA, hq)
