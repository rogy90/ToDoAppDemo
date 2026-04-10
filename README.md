# ToDoAppDemo

Automated end-to-end tests for the [TodoMVC](https://demo.playwright.dev/todomvc/#/) demo application using **Playwright for Python**.

## Test Coverage

- Adding todos with English text
- Adding todos with non-English characters (Unicode)
- Adding todos with numbers
- Marking todos as complete
- Deleting todos
- Filtering by "Active" todos
- Filtering by "Completed" todos

## Project Structure

```
├── README.md          # This file
├── requirements.txt   # Python dependencies
├── pytest.ini         # Pytest configuration
├── conftest.py        # Shared fixtures
├── ruff.toml          # Ruff configuration
├── mypy.ini           # MyPy configuration
├── pages/
│   ├── __init__.py
│   └── todo_page.py   # Page Object Model
└── tests/
    ├── __init__.py
    └── test_todo.py   # Test cases
```

## Installation

```bash
git clone https://github.com/rogy90/ToDoAppDemo.git
cd ToDoAppDemo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Running Tests

```bash
pytest
pytest -v
pytest --headed
pytest -k test_add_todo_english
pytest --html=report.html --self-contained-html
```

## Code Quality

```bash
ruff check . --fix
ruff format .
mypy .
```

## CI/CD

GitHub Actions workflow is in `.github/workflows/test.yml`.

## License

MIT
