# FullStackAutomationTests

### Usage & Maintenance

#### Setup
```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows
pip install -r requirements.txt
playwright install
```

#### Running tests
```bash
pytest -m ui                    # Run UI tests
pytest -m api                   # Run API tests
pytest                          # Run all
```

Optional flags:
```bash
--headless                      # Run without browser UI
--resolution=1920x1080          # Set viewport size
--browser=chromium|firefox|webkit
--html=reports/report.html      # HTML report output
```

#### Environment config
Set API and UI endpoints in `.env`:
```
UI_BASE=https://the-internet.herokuapp.com
API_BASE=https://jsonplaceholder.typicode.com
```

#### Maintenance
- All reports are saved to `reports/report.html`
- Use `env_settings` for centralizing `.env` access
- Fixtures autoload via `conftest.py` (no import needed)
- Add new test files in `tests/` directory following `test_*.py` pattern

