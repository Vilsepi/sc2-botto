import random
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from bot.main import MyBot


if __name__ == "__main__":
    bot = Bot(Race.Zerg, MyBot())
    run_game(
        random.choice(maps.get()),
        [bot, Computer(Race.Random, Difficulty.Hard)],
        realtime=False,
        step_time_limit=0.1,
        game_time_limit=(60 * 60),
        save_replay_as="latest.SC2Replay",
    )
