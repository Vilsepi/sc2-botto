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


def should_build(bot: sc2.BotAI, hq: Unit, unit_type) -> bool:
    if unit_type == UnitTypeId.SPAWNINGPOOL:
        return (
            bot.structures(UnitTypeId.SPAWNINGPOOL).amount
            + bot.already_pending(UnitTypeId.SPAWNINGPOOL)
            == 0
        )
    elif unit_type == UnitTypeId.LAIR:
        return (
            bot.structures(UnitTypeId.SPAWNINGPOOL).ready
            and hq.is_idle
            and not bot.townhalls(UnitTypeId.LAIR)
        )
    elif unit_type == UnitTypeId.HYDRALISKDEN:
        return bot.townhalls(UnitTypeId.LAIR).ready and (
            bot.structures(UnitTypeId.HYDRALISKDEN).amount
            + bot.already_pending(UnitTypeId.HYDRALISKDEN)
            == 0
        )
    elif unit_type == UnitTypeId.EXTRACTOR:
        return (
            bot.structures(UnitTypeId.SPAWNINGPOOL)
            and bot.gas_buildings.amount + bot.already_pending(UnitTypeId.EXTRACTOR) < 2
        )
    else:
        return False


async def do_build(bot: sc2.BotAI, hq: Unit, unit_type):
    bot.logger.info(f"Building {unit_type}")
    if unit_type == UnitTypeId.LAIR:
        upgrade_building(hq, UnitTypeId.LAIR)
    elif unit_type == UnitTypeId.EXTRACTOR:
        build_gas_extractor(bot, hq)
    else:
        await build_building_in_hq(bot, hq, unit_type)


async def build_building_in_hq(bot: sc2.BotAI, hq: Unit, unit_type):
    """Build a single building near hq with no exact position"""
    await bot.build(
        unit_type,
        near=hq.position.towards(bot.game_info.map_center, 5),
    )


def build_gas_extractor(bot: sc2.BotAI, base: Unit):
    for geyser in bot.vespene_geyser.closer_than(10, base):
        # TODO: We should pick a worker only from this base
        workers: Units = bot.workers
        if workers:
            bot.workers.random.build_gas(geyser)
            break


def upgrade_building(building: Unit, upgrade_to):
    """Upgrade an existing building to another phase (e.g Lair to Hive)"""
    building.build(upgrade_to)


async def build_structures(bot: sc2.BotAI, hq: Unit):
    for building in BUILDING_PRIORITY:
        if bot.can_afford(building) and should_build(bot, hq, building):
            await do_build(bot, hq, building)
            return
