import logging
import re

try:
    import colorama
    from colorama import Fore, Style

    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class ColoredFormatter(logging.Formatter):
    if COLORAMA_AVAILABLE:
        level_to_color = {
            "DEBUG": Fore.BLUE + Style.BRIGHT,
            "INFO": Fore.GREEN + Style.BRIGHT,
            "WARNING": Fore.YELLOW + Style.BRIGHT,
            "ERROR": Fore.RED + Style.BRIGHT,
            "CRITICAL": Fore.RED + Style.BRIGHT + Style.BRIGHT,
        }
    else:
        level_to_color = {}

    def format(self, record):
        color = self.level_to_color.get(record.levelname, "")
        message = super().format(record)
        if COLORAMA_AVAILABLE:
            return color + message + Style.RESET_ALL
        else:
            return message


def setup_logger(
    name: str = __name__,
    level: int = logging.INFO,
    colored: bool = True,
    verbose: bool = False,
) -> logging.Logger:
    """
    Sets up a logger with optional coloring and debug-level verbose information.
    """
    logger = logging.getLogger(name)
    final_level = logging.DEBUG if verbose else level
    logger.setLevel(final_level)

    debug_info = (
        " (%(filename)s:%(lineno)d:%(funcName)s)"
        if final_level == logging.DEBUG
        else ""
    )
    log_format = f"%(asctime)s [%(levelname)s]{debug_info} %(message)s "
    datefmt = "%Y-%m-%d %H:%M:%S"

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(final_level)
        if colored and COLORAMA_AVAILABLE:
            formatter = ColoredFormatter(log_format, datefmt=datefmt)
        else:
            formatter = logging.Formatter(log_format, datefmt=datefmt)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


def camel_to_snake(s: str) -> str:
    """Converts input string from CamelCase to snake_case."""
    return (
        re.sub(r"(?<!^)(?=[A-Z])", "_", s)  # insert underscores before capital letters
        .replace(" ", "_")  # fix non non-standard CamelCase inputs
        .replace("__", "_")  # fix double underscores (from previous replace)
        .lower()  # lowercase for true snake_case
    )
