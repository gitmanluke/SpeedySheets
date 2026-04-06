# SpeedySheets

SpeedySheets is a CLI tool for loading CSV data into SQLite, running SQL queries, and asking natural-language questions that get translated into SQL.

## Prerequisites

- Python 3.10+
- An Anthropic API key (required only for `ask`)

## Setup

1. Clone the repository and move into the project directory:
   - `git clone <your-repo-url>`
   - `cd SpeedySheets`
2. Install dependencies:
   - `python -m pip install -r requirements.txt`
3. Set your Anthropic API key (needed for `ask`):
   - PowerShell (current session): `$env:ANTHROPIC_API_KEY="your_api_key_here"`
   - Bash/zsh: `export ANTHROPIC_API_KEY="your_api_key_here"`

## CLI Commands

Run all commands from the project root.

### 1) Initialize database path (required first)

- `python interface.py init data/database.db`

This saves the active DB path to `.speedysheets.json` so later commands use the same database automatically.

### 2) Upload CSV data into a table

- Single file:
  - `python interface.py upload data/orders.csv orders`
- Multiple file/table pairs:
  - `python interface.py upload data/orders.csv orders data/health.csv health`

### 3) Run SQL directly

- `python interface.py query "SELECT * FROM orders LIMIT 5"`

Notes:
- Only read-only `SELECT` queries are allowed.
- Queries are validated before execution.

### 4) Ask a natural-language question

- `python interface.py ask "What are the addresses of people with height over 50?"`

## Typical Run Order

1. `python interface.py init data/database.db`
2. `python interface.py upload data/orders.csv orders`
3. `python interface.py query "SELECT * FROM orders LIMIT 5"`
4. `python interface.py ask "Which customers placed the largest orders?"`

## Troubleshooting

- **"No database configured"**
  - Run `python interface.py init <db_path>` first.

- **`ask` returns invalid query**
  - Confirm `ANTHROPIC_API_KEY` is set.
  - Confirm your tables/columns exist in the configured DB.