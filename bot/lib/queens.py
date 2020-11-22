from bot.util.logging import TerminalLogger
import sc2
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId


class QueenManager:
    def __init__(self, bot: sc2.BotAI) -> None:
        self.bot = bot
        self.logger: TerminalLogger = bot.logger

    def manage_queens(self):
        for queen in self.bot.units(UnitTypeId.QUEEN).idle:
            if queen.energy >= 25:
                closest_townhall = self.bot.townhalls.closest_to(queen)
                queen(AbilityId.EFFECT_INJECTLARVA, closest_townhall)
                self.logger.info("Queen injecting larvae")
