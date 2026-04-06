#data: takes in a user request
# either a 'query' or 'input'

#controls: first determine what the user is trying to do,
# either uploading data or making a query
# if the user is uploading data, send the information to the dataLoader
# if the user is making a query, send the information to the queryService

#status: invalid request, query successfully sent, input successfully sent
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click

from dataLoader.loadCSV import dataLoader
from queryService.handleQuery import handleQuery
from schemaManager.schemaManager import schemaManager


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
    obj["query_handler"] = handleQuery(obj["schema_manager"])
    click.echo(f"Database initialized at {db_path}")


@cli.command()
@click.argument("data_pairs", nargs=-1, required=True)
@click.pass_obj
def upload(obj, data_pairs):
    """Upload one or more CSV files to the database.
    
    Usage: upload data1.csv health data2.csv orders
    """
    if len(data_pairs) % 2 != 0:
        raise click.UsageError("Each file must have a matching table name: upload data1.csv health data2.csv orders")
    
    pairs = zip(data_pairs[::2], data_pairs[1::2])
    for data_path, table_name in pairs:
        print(f"Uploading {data_path} as table '{table_name}'")
        obj["data_loader"].send_to_manager(data_path, table_name)


@cli.command()
@click.argument("query")
@click.pass_obj
def query(obj, query):
    """Execute a SQL query."""
    result = obj["query_handler"].execute_SQL(query)
    click.echo(result)


@cli.command()
@click.argument("question")
@click.pass_obj
def ask(obj, question):
    """Ask a natural language question."""
    result = obj["query_handler"].send_to_LLM(obj["schema_manager"],question)
    click.echo(result)


if __name__ == "__main__":
    cli()
# def main():
#     @click.command()
#     def upload(count, name):
#         print(f'HELLO')
        

#     # if args.command == 'upload':
#     #     loader.send_to_manager(args.files)
#     # elif args.command == 'query':
#     #     result = query_handler.execute_SQL(args.sql)
#     #     print(result)
#     # elif args.command == 'ask':
#     #     question = ' '.join(args.question)
#     #     result = query_handler.send_to_LLM(question)
#     #     print(result)

# if __name__ == '__main__':
#     main()
#     upload()
