from sc2.data import Result
import sc2
from bot.lib.army import ArmyManager
from bot.lib.build import BuildManager
from bot.lib.overlords import OverlordManager
from bot.lib.queens import QueenManager
from bot.lib.train import UnitTrainingManager
from bot.lib.upgrades import UpgradeManager
from bot.lib.workers import WorkerManager
from bot.util.logging import TerminalLogger


class Botto(sc2.BotAI):
    async def on_start(self):
        self.logger: TerminalLogger = TerminalLogger(self)
        self.army_manager: ArmyManager = ArmyManager(self)
        self.build_manager: BuildManager = BuildManager(self, self.logger)
        self.train_manager: UnitTrainingManager = UnitTrainingManager(self, self.logger)
        self.worker_manager: WorkerManager = WorkerManager(self)
        self.upgrade_manager: UpgradeManager = UpgradeManager(self, self.logger)
        self.overlord_manager: OverlordManager = OverlordManager(self)
        self.queen_manager: QueenManager = QueenManager(self, self.logger)

    async def on_step(self, iteration: int):
        self.army_manager.manage_army(iteration)
        if self.train_manager.manage_unit_training_from_larvae():
            return
        self.train_manager.manage_queen_training()
        self.upgrade_manager.manage_tech_upgrades()
        await self.build_manager.manage_build_projects()
        self.worker_manager.manage_workers()
        self.queen_manager.manage_queens()
        self.overlord_manager.manage_overlords()
        self.train_manager.set_hatchery_rally_points(iteration)

    async def on_end(
        self, game_result: Result
    ):  # pyright: reportGeneralTypeIssues=false
        self.logger.log_end_stats(game_result)
