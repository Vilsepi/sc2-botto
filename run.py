import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer


class WorkerRushBot(sc2.BotAI):
    async def on_step(self, iteration: int):
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])


if __name__ == '__main__':
    run_game(
        maps.get("Abyssal Reef LE"),
        [
            Bot(Race.Protoss, WorkerRushBot()),
            Computer(Race.Protoss, Difficulty.VeryEasy)
        ],
        realtime=False,
        step_time_limit=0.5,
        game_time_limit=(60*60),
        save_replay_as="latest.SC2Replay"
    )
