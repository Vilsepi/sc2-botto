import sc2
from sc2.units import Units


def assign_workers(bot: sc2.BotAI):
    # Saturate gas
    for gas in bot.gas_buildings:
        if gas.assigned_harvesters < gas.ideal_harvesters:
            workers: Units = bot.workers.closer_than(10, gas)
            if workers:
                workers.random.gather(gas)
