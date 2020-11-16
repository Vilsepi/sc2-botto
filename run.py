from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from bot.main import MyBot


if __name__ == '__main__':
    bot = Bot(Race.Protoss, MyBot())
    run_game(
        maps.get("Abyssal Reef LE"),
        [bot, Computer(Race.Protoss, Difficulty.VeryEasy)],
        realtime=False,
        step_time_limit=0.5,
        game_time_limit=(60*60),
        save_replay_as="latest.SC2Replay"
    )
