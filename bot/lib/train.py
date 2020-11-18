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


def should_train(bot: sc2.BotAI, unit_type) -> bool:
    if unit_type == UnitTypeId.OVERLORD:
        return bot.supply_left < 2
    elif unit_type == UnitTypeId.HYDRALISK:
        return bot.structures(UnitTypeId.HYDRALISKDEN).ready
    elif unit_type == UnitTypeId.DRONE:
        return bot.supply_workers + bot.already_pending(UnitTypeId.DRONE) < 22
    elif unit_type == UnitTypeId.ZERGLING:
        return bot.units(UnitTypeId.ZERGLING).amount < 20 and bot.minerals > 1000
    else:
        return False


def train_units_from_larvae(bot: sc2.BotAI) -> bool:
    larvae: Units = bot.larva
    if larvae:
        larva: Unit = larvae.random
        for unit in TRAINING_PRIORITY:
            if bot.can_afford(unit) and should_train(bot, unit):
                larva.train(unit)
                return True
    return False


def train_queen(bot: sc2.BotAI, townhall: Unit):
    if bot.structures(UnitTypeId.SPAWNINGPOOL).ready:
        if not bot.units(UnitTypeId.QUEEN) and townhall.is_idle:
            if bot.can_afford(UnitTypeId.QUEEN):
                townhall.train(UnitTypeId.QUEEN)
