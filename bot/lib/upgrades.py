from bot.util.logging import TerminalLogger
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId


class UpgradeManager:
    def __init__(self, bot: sc2.BotAI, logger: TerminalLogger):
        self.bot = bot
        self.logger: TerminalLogger = logger

    # If hydra den is ready and idle, research upgrades
    def manage_tech_upgrades(self):
        hydra_dens = self.bot.structures(UnitTypeId.HYDRALISKDEN)
        if hydra_dens:
            for hydra_den in hydra_dens.ready.idle:
                if self.bot.already_pending_upgrade(
                    UpgradeId.EVOLVEGROOVEDSPINES
                ) == 0 and self.bot.can_afford(UpgradeId.EVOLVEGROOVEDSPINES):
                    self.logger.info("Researching grooved spines")
                    hydra_den.research(UpgradeId.EVOLVEGROOVEDSPINES)
                elif self.bot.already_pending_upgrade(
                    UpgradeId.EVOLVEMUSCULARAUGMENTS
                ) == 0 and self.bot.can_afford(UpgradeId.EVOLVEMUSCULARAUGMENTS):
                    self.logger.info("Researching muscular augments")
                    hydra_den.research(UpgradeId.EVOLVEMUSCULARAUGMENTS)
