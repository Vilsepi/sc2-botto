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


class MyBot(sc2.BotAI):
    async def on_start(self):
        self.iteration = 0

    async def on_step(self, iteration):
        self.iteration = iteration

        """ print("A={} B={} C={} D={} E={} F={} G={} H={}".format(
            iteration,
            self._time_before_step,
            self._time_after_step,
            self._min_step_time,
            self._max_step_time,
            self._last_step_step_time,
            self._total_time_in_on_step,
            self._total_steps_iterations)) """

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
        print(
            f"Game ended in {result} with score {self.state.score.score} at iteration {self._total_steps_iterations} with step times {self.step_time}"
        )
