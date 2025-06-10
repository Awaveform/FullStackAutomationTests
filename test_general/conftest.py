from pathlib import Path

import pytest
from _pytest.config import Config
from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def pytest_configure(config: Config) -> None:
    config.option.htmlpath = str(REPORTS_DIR / "report.html")


def validate_response(model, data, raise_on_error=True):
    """
    Validate API response against a pydantic model; fail or raise on error
    based on a flag.
    """
    try:
        return model.model_validate(data)
    except ValidationError as e:
        if raise_on_error:
            snippet = (
                    str(data)[:300] + "..."
            ) if len(str(data)) > 300 else str(data)
            pytest.fail(f"Validation failed for data: {snippet}\n{e}")
        else:
            raise
