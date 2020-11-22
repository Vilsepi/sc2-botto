import sc2
from sc2.units import Units


class WorkerManager:
    def __init__(self, bot: sc2.BotAI):
        self.bot = bot

    def manage_workers(self):
        # Saturate gas
        for gas in self.bot.gas_buildings:
            if gas.assigned_harvesters < gas.ideal_harvesters:
                workers: Units = self.bot.workers.closer_than(10, gas)
                if workers:
                    workers.random.gather(gas)
