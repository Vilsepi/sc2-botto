import sc2
from sc2.unit import Unit
from bot.lib.army import ArmyManager
from bot.lib.build import BuildManager
from bot.lib.queens import QueenManager
from bot.lib.train import UnitTrainingManager
from bot.lib.upgrades import UpgradeManager
from bot.lib.workers import WorkerManager
from bot.util.logging import TerminalLogger


class MyBot(sc2.BotAI):
    async def on_start(self):
        self.logger: TerminalLogger = TerminalLogger(self)
        self.army_manager: ArmyManager = ArmyManager(self)
        self.build_manager: BuildManager = BuildManager(self)
        self.train_manager: UnitTrainingManager = UnitTrainingManager(self)
        self.worker_manager: WorkerManager = WorkerManager(self)
        self.upgrade_manager: UpgradeManager = UpgradeManager(self)
        self.queen_manager: QueenManager = QueenManager(self)

    async def on_step(self, iteration):
        if self.townhalls:
            hq: Unit = self.townhalls.first
        else:
            self.army_manager.manage_final_assault()
            return
        self.army_manager.manage_army(iteration % 50 == 0)
        if self.train_manager.manage_unit_training_from_larvae():
            return
        self.train_manager.manage_queen_training(hq)
        self.upgrade_manager.manage_tech_upgrades()
        self.queen_manager.manage_queens(hq)
        await self.build_manager.manage_build_projects(hq)
        self.worker_manager.manage_workers()

    async def on_end(self, result):
        self.logger.info(
            f"Game ended in {result} with score {self.state.score.score} at iteration {self._total_steps_iterations} with step times {self.step_time}"
        )
