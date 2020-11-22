import sc2
from sc2.ids.unit_typeid import UnitTypeId


class OverlordManager:
    def __init__(self, bot: sc2.BotAI) -> None:
        self.bot = bot

    def manage_overlords(self):
        """Scout the borders of our bases with our overlords"""
        overlords = self.bot.units(UnitTypeId.OVERLORD)
        if overlords.amount == 1:
            overlords.first.move(self.bot.main_base_ramp.top_center)
        elif overlords.amount > 1:
            for overlord in overlords.idle:
                closest_townhall = self.bot.townhalls.closest_to(overlord)
                overlord.move(closest_townhall.position.random_on_distance(20))
