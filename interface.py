#data: takes in a user request
# either a 'query' or 'input'

#controls: first determine what the user is trying to do,
# either uploading data or making a query
# if the user is uploading data, send the information to the dataLoader
# if the user is making a query, send the information to the queryService

#status: invalid request, query successfully sent, input successfully sent
import click
import json
from pathlib import Path

from dataLoader.loadCSV import dataLoader
from queryService.handleQuery import handleQuery
from schemaManager.schemaManager import schemaManager

CONFIG_FILE_NAME = ".speedysheets.json"


def _get_config_path():
    return Path(__file__).resolve().parent / CONFIG_FILE_NAME


def _save_db_path(db_path):
    config_path = _get_config_path()
    config_path.write_text(json.dumps({"database_path": db_path}, indent=2), encoding="utf-8")


def _load_db_path():
    config_path = _get_config_path()
    if not config_path.exists():
        raise click.ClickException("No database configured. Run: python interface.py init <db_path>")

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid config file at {config_path}: {exc}") from exc

    db_path = config.get("database_path")
    if not db_path:
        raise click.ClickException("Config missing 'database_path'. Run: python interface.py init <db_path>")
    return db_path


def _set_active_database(obj):
    db_path = _load_db_path()
    obj["schema_manager"].set_database(db_path)
    if obj["schema_manager"].cursor is None:
        raise click.ClickException(f"Failed to open configured database: {db_path}")
    obj["query_handler"] = handleQuery(obj["schema_manager"])
    return db_path


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    schema_manager = schemaManager()
    ctx.obj = {
        "schema_manager": schema_manager,
        "data_loader": dataLoader(schema_manager),
        "query_handler": None,
    }

@cli.command()
@click.argument("db_path")
@click.pass_obj
def init(obj, db_path):
    """Initialize the database at the given path."""
    obj["schema_manager"].set_database(db_path)
    if obj["schema_manager"].cursor is None:
        raise click.ClickException(f"Failed to open database at {db_path}")
    _save_db_path(db_path)
    obj["query_handler"] = handleQuery(obj["schema_manager"])
    click.echo(f"Database initialized at {db_path}")
    click.echo(f"Saved default database config at {_get_config_path()}")


@cli.command()
@click.argument("data_pairs", nargs=-1, required=True)
@click.pass_obj
def upload(obj, data_pairs):
    """Upload one or more CSV files to the database.
    
    Usage: upload data1.csv health data2.csv orders
    """
    db_path = _set_active_database(obj)

    if len(data_pairs) % 2 != 0:
        raise click.UsageError("Each file must have a matching table name: upload data1.csv health data2.csv orders")
    
    pairs = zip(data_pairs[::2], data_pairs[1::2])
    for data_path, table_name in pairs:
        print(f"Uploading {data_path} as table '{table_name}'")
        print(f"Database path: {db_path}")
        obj["data_loader"].send_to_manager(data_path, db_path, table_name)


@cli.command()
@click.argument("query")
@click.pass_obj
def query(obj, query):
    """Execute a SQL query."""
    _set_active_database(obj)
    result = obj["query_handler"].execute_SQL(query)
    click.echo(result)


@cli.command()
@click.argument("question")
@click.pass_obj
def ask(obj, question):
    """Ask a natural language question."""
    _set_active_database(obj)
    result = obj["query_handler"].send_to_LLM(question)
    click.echo(result)


if __name__ == "__main__":
    cli()