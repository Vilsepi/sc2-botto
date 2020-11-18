import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId


# If hydra den is ready and idle, research upgrades
def upgrade_unit_tech(bot: sc2.BotAI):
    hydra_dens = bot.structures(UnitTypeId.HYDRALISKDEN)
    if hydra_dens:
        for hydra_den in hydra_dens.ready.idle:
            if bot.already_pending_upgrade(
                UpgradeId.EVOLVEGROOVEDSPINES
            ) == 0 and bot.can_afford(UpgradeId.EVOLVEGROOVEDSPINES):
                hydra_den.research(UpgradeId.EVOLVEGROOVEDSPINES)
            elif bot.already_pending_upgrade(
                UpgradeId.EVOLVEMUSCULARAUGMENTS
            ) == 0 and bot.can_afford(UpgradeId.EVOLVEMUSCULARAUGMENTS):
                hydra_den.research(UpgradeId.EVOLVEMUSCULARAUGMENTS)
