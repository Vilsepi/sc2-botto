from loguru import logger
import sc2
from sc2.data import Result


class TerminalLogger:
    """Provides unified logging facilities with extra game info in each message"""

    def __init__(self, bot: sc2.BotAI):
        self.bot = bot

    def _prefix_message(self, message: str) -> str:
        """Prefixes each log message with game time in minutes, unit supply cap usage, and unit supply cap"""
        if hasattr(self.bot, "state"):
            return "{:4.1f} {:3}/{:<3} {}".format(
                self.bot.time / 60,
                self.bot.supply_used,
                self.bot.supply_cap,
                message,
            )
        else:
            return "--.- --- ---/--- " + message

    def error(self, message: str):
        logger.error(self._prefix_message(message))

    def warning(self, message: str):
        logger.warning(self._prefix_message(message))

    def info(self, message: str):
        logger.info(self._prefix_message(message))

    def debug(self, message: str):
        logger.debug(self._prefix_message(message))

    def log_end_stats(
        self, game_result: Result
    ):  # pyright: reportGeneralTypeIssues=false
        score: int = (
            self.bot.state.score.score
        )  # pyright: reportUnknownMemberType=false
        steps: int = (
            self.bot._total_steps_iterations
        )  # pyright: reportPrivateUsage=false
        logger.info(
            f"Game ended in {game_result} with score {score} at iteration {steps} with step times {self.bot.step_time}"
        )
