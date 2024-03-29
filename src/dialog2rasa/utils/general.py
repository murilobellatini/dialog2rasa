import logging
import re
from logging import INFO, Logger, StreamHandler


def setup_logger() -> Logger:
    """Sets up the logger configuration."""
    # Format string including level, module, and function name
    format_str = "%(levelname)s - %(module)s - %(funcName)s - %(message)s"

    # Create and configure logger
    logger = logging.getLogger()
    logger.setLevel(INFO)

    # Create console handler and set level to info
    ch = StreamHandler()
    ch.setLevel(INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(format_str)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)
    return logger


logger = setup_logger()


def camel_to_snake(s: str) -> str:
    """Converts input string from CamelCase to snake_case."""
    return (
        re.sub(r"(?<!^)(?=[A-Z])", "_", s)  # insert underscores before capital letters
        .replace(" ", "_")  # fix non non-standard CamelCase inputs
        .replace("__", "_")  # fix double underscores (from previous replace)
        .lower()  # lowercase for true snake_case
    )
