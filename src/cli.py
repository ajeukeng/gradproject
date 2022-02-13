import click
from covidVisualizationTool.imports.importData import ImportData as ID
import common_utilities as cu
from covidVisualizationTool.queries.queryData import QueryData as QD


@click.group()
def cvt():
    # Name for the Covid Visualization Tool
    pass


@cvt.command()
@click.argument('csv_location')
@click.argument('db_name')
def import_data(csv_location, db_name: str):
    # Import Covid Dataset
    if cu.check_path(csv_location):
        # id_covid = ID(csv_location, db_name)
        # id_covid.load_tables()
        query_stuff = QD(db_location=db_name)
        query_stuff.get_all_data()
    else:
        print("Unable to find path")
