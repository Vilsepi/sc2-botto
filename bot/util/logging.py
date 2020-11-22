from loguru import logger
import sc2


class TerminalLogger:
    def __init__(self, bot: sc2.BotAI):
        self.bot = bot

    def _prefix_message(self, message: str):
        try:
            if hasattr(self.bot, "state"):
                return "{:4.1f} {:3}/{:<3} {}".format(
                    self.bot.time / 60,
                    self.bot.supply_used,
                    self.bot.supply_cap,
                    message,
                )
            else:
                return "--.- --- ---/--- " + message
        except Exception as e:
            print("ERROR WHILE LOGGING:", message, e)

    def error(self, message: str):
        logger.error(self._prefix_message(message))

    def warning(self, message: str):
        logger.warning(self._prefix_message(message))

    def info(self, message: str):
        logger.info(self._prefix_message(message))

    def debug(self, message: str):
        logger.debug(self._prefix_message(message))
