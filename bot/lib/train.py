from bot.util.logging import TerminalLogger
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units


TRAINING_PRIORITY = [
    UnitTypeId.OVERLORD,
    UnitTypeId.HYDRALISK,
    UnitTypeId.DRONE,
    UnitTypeId.ZERGLING,
]


class UnitTrainingManager:
    def __init__(self, bot: sc2.BotAI) -> None:
        self.bot = bot
        self.logger: TerminalLogger = bot.logger

    def _should_train(self, unit_type) -> bool:
        if unit_type == UnitTypeId.OVERLORD:
            return self.bot.supply_left < 2
        elif unit_type == UnitTypeId.HYDRALISK:
            return self.bot.structures(UnitTypeId.HYDRALISKDEN).ready
        elif unit_type == UnitTypeId.DRONE:
            return (
                self.bot.supply_workers + self.bot.already_pending(UnitTypeId.DRONE)
                < 22
            )
        elif unit_type == UnitTypeId.ZERGLING:
            return (
                self.bot.units(UnitTypeId.ZERGLING).amount < 20
                and self.bot.minerals > 1000
            )
        else:
            return False

    def manage_unit_training_from_larvae(self) -> bool:
        larvae: Units = self.bot.larva
        if larvae:
            larva: Unit = larvae.random
            for unit in TRAINING_PRIORITY:
                if self.bot.can_afford(unit) and self._should_train(unit):
                    self.logger.info(f"Training {unit}")
                    larva.train(unit)
                    return True
        return False

    def manage_queen_training(self):
        if self.bot.structures(UnitTypeId.SPAWNINGPOOL).ready:
            if not self.bot.units(UnitTypeId.QUEEN) and self.bot.can_afford(
                UnitTypeId.QUEEN
            ):
                for townhall in self.bot.townhalls:
                    if townhall.is_idle:
                        townhall.train(UnitTypeId.QUEEN)
                        return
