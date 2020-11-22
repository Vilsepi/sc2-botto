import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.units import Units
from .lib import army
from .lib import build
from .lib import train
from .lib import upgrades
from .lib import workers
from .util.logging import TerminalLogger


class MyBot(sc2.BotAI):
    def __init__(self) -> None:
        self.logger: TerminalLogger = None

    async def on_start(self):
        self.iteration = 0
        self.logger: TerminalLogger = TerminalLogger(self)

    async def on_step(self, iteration):
        self.iteration = iteration

        forces: Units = self.units.of_type({UnitTypeId.ZERGLING, UnitTypeId.HYDRALISK})
        if self.townhalls:
            hq: Unit = self.townhalls.first
        else:
            army.final_assault(self)
            return

        army.attack_base(self, forces, iteration % 50 == 0)

        if train.train_units_from_larvae(self):
            return
        train.train_queen(self, hq)

        upgrades.upgrade_unit_tech(self)

        for queen in self.units(UnitTypeId.QUEEN).idle:
            if queen.energy >= 25:
                queen(AbilityId.EFFECT_INJECTLARVA, hq)

        await build.build_structures(self, hq)

        workers.assign_workers(self)

    async def on_end(self, result):
        self.logger.info(
            f"Game ended in {result} with score {self.state.score.score} at iteration {self._total_steps_iterations} with step times {self.step_time}"
        )
