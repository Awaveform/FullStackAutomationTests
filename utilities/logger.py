import json
from datetime import datetime
from pathlib import Path
from typing import Callable

from loguru import logger
from loguru._handler import Message

from utilities.env_settings import env_settings

# log directory and file path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
log_path = PROJECT_ROOT / "reports"

log_path.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = log_path / f"log_{timestamp}.json"

# log level from environment variable
log_level = env_settings.LOG_LEVEL


def make_sink(log_file: Path) -> Callable[[Message], None]:
    """
    Creates a simplified JSON log sink that writes log entries
    with timestamp, level, and message.

    :param log_file: Path where log entries will be saved
    :return: A sink function compatible with loguru
    """

    def sink(message: Message) -> None:
        """
        Formats and writes a single log message to file.

        :param message: Loguru Message object containing log data
        """
        record = message.record
        data = {
            "time": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "level": record["level"].name,
            "message": record["message"],
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

    return sink


# loguru handler to avoid duplicate output
logger.remove()

# custom log handler with selected log level
logger.add(
    make_sink(log_file),
    level=log_level
)

# export the configured logger
log = logger
