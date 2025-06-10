# FullStackAutomationTests

A hybrid UI/API test suite using `pytest`, `Playwright`, and `requests`.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/FullStackAutomationTests.git
cd FullStackAutomationTests
```

### 2. Setup Python Environment (Windows)

```bash
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

> Make sure Python 3.12+ is installed and added to PATH.

### 3. Configure Environment

Create a `.env` file (already present in repo) and adjust if needed:

```ini
UI_BASE = https://the-internet.herokuapp.com/
API_BASE = https://jsonplaceholder.typicode.com/
PLAYWRIGHT_TIMEOUT = 10000
PLAYWRIGHT_SLOWMO = 1000
LOG_LEVEL = INFO
```

---

## Running Tests

### All Tests

```bash
pytest
```

### API Tests Only

```bash
pytest -m api
```

### UI Tests Only

```bash
pytest -m ui
```

### Run With Report

```bash
pytest --html=reports/report.html --self-contained-html
```

> Reports are saved in the `reports/` folder.

---

## Optional Flags

```bash
--headless                   # Run browser without UI (default)
--browser=chromium|firefox|webkit
--html=reports/report.html   # Save HTML report
-v                          # Verbose output
```

---

## Project Structure

```
.
├── tests/
│   ├── test_get_posts.py
│   ├── test_create_posts.py
│   ├── test_upload_file.py
│   └── ...
├── pages/
├── reports/
├── utilities/
│   └── env_settings.py
├── models.py
├── .env
├── pytest.ini
└── README.md
```

---

## Notes

- Test data lives in `tests/_test_data/`
- Upload scenarios use POM: see `UploadPage` in `pages/`
- API validations use `pydantic` schemas from `models.py`
- `conftest.py` auto-loads common fixtures and Playwright hooks
- HTML reports and video recordings are saved in `reports/`

---

## Maintenance Tips

- Use `env_settings` for environment variable access
- Group tests with `@pytest.mark.api` or `@pytest.mark.ui`
- Use `Post` / `PostList` for API schema validation
- Keep `.env` secrets private (don’t commit sensitive keys)
