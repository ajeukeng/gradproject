import click
from CovidVIsualizationTool import CovidVisualizationTool as CVT
from imports.importData import ImportData as ID
import common_utilities as cu


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
        id_covid = ID(csv_location, db_name)
        id_covid.load_tables()
    else:
        print("Unable to find path")
