import json
from datetime import datetime
from pathlib import Path

from loguru import logger

# log paths
log_path = Path(__file__).resolve().parent.parent / "reports"
log_path.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
debug_log_file = log_path / f"debug_{timestamp}.json"
info_log_file = log_path / f"info_{timestamp}.json"


def make_debug_sink(log_file):
    def sink(message):
        record = message.record
        data = {
            "time": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "level": record["level"].name,
            "test": record["name"],
            "function": record["function"],
            "file": record["file"].path,
            "line": record["line"],
            "elapsed": f"{record['elapsed'].total_seconds():.3f}s",
            "message": record["message"],
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2) + "\n")

    return sink


def make_info_sink(log_file):
    def sink(message):
        record = message.record
        data = {
            "time": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "level": record["level"].name,
            "test": record["name"],
            "function": record["function"],
            "message": record["message"],
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2) + "\n")

    return sink


logger.remove()

# Debug sink
logger.add(
    make_debug_sink(debug_log_file),
    level="DEBUG",
    filter=lambda record: record["level"].name == "DEBUG"
)

# Info sink
logger.add(
    make_info_sink(info_log_file),
    level="INFO",
    filter=lambda record: record["level"].name == "INFO"
)

log = logger
