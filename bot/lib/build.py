from bot.util.logging import TerminalLogger
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units


BUILDING_PRIORITY = [
    UnitTypeId.SPAWNINGPOOL,
    UnitTypeId.LAIR,
    UnitTypeId.HYDRALISKDEN,
    UnitTypeId.EXTRACTOR,
]


class BuildManager:
    def __init__(self, bot: sc2.BotAI, logger: TerminalLogger):
        self.bot = bot
        self.logger: TerminalLogger = logger

    def _should_build(self, hq: Unit, unit_type: UnitTypeId) -> bool:
        if unit_type == UnitTypeId.SPAWNINGPOOL:
            return (
                self.bot.structures(UnitTypeId.SPAWNINGPOOL).amount
                + self.bot.already_pending(UnitTypeId.SPAWNINGPOOL)
                == 0
            )
        elif unit_type == UnitTypeId.LAIR:
            return (
                self.bot.structures(UnitTypeId.SPAWNINGPOOL).ready.exists
                and hq.is_idle
                and not self.bot.townhalls(UnitTypeId.LAIR)
            )
        elif unit_type == UnitTypeId.HYDRALISKDEN:
            return self.bot.townhalls(UnitTypeId.LAIR).ready.exists and (
                self.bot.structures(UnitTypeId.HYDRALISKDEN).amount
                + self.bot.already_pending(UnitTypeId.HYDRALISKDEN)
                == 0
            )
        elif unit_type == UnitTypeId.EXTRACTOR:
            return (
                self.bot.structures(UnitTypeId.SPAWNINGPOOL).exists
                and self.bot.gas_buildings.amount
                + self.bot.already_pending(UnitTypeId.EXTRACTOR)
                < 2
            )
        else:
            return False

    async def _do_build(self, hq: Unit, unit_type: UnitTypeId):
        self.logger.info(f"Building {unit_type}")
        if unit_type == UnitTypeId.LAIR:
            self._upgrade_building(hq, UnitTypeId.LAIR)
        elif unit_type == UnitTypeId.EXTRACTOR:
            self._build_gas_extractor(hq)
        else:
            await self._build_building_in_hq(hq, unit_type)

    async def _build_building_in_hq(self, hq: Unit, unit_type: UnitTypeId):
        """Build a single building near hq with no exact position"""
        await self.bot.build(
            unit_type,
            near=hq.position.towards(self.bot.game_info.map_center, 5),
        )

    def _build_gas_extractor(self, base: Unit):
        for geyser in self.bot.vespene_geyser.closer_than(10, base):
            # TODO: We should pick a worker only from this base
            workers: Units = self.bot.workers
            if workers:
                self.bot.workers.random.build_gas(geyser)
                break

    def _upgrade_building(self, building: Unit, upgrade_to: UnitTypeId):
        """Upgrade an existing building to another phase (e.g Lair to Hive)"""
        building.build(upgrade_to)

    async def manage_build_projects(self):
        if self.bot.townhalls:
            hq: Unit = self.bot.townhalls.first
            for building in BUILDING_PRIORITY:
                if self.bot.can_afford(building) and self._should_build(hq, building):
                    await self._do_build(hq, building)
                    return
