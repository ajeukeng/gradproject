import click
from CovidVIsualizationTool import CovidVisualizationTool as CVT
from imports.importData import ImportData as ID
import common_utilities as cu
import getpass


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
        db_pwd = click.prompt("Enter password for database: ")
        id_covid = ID(csv_location, db_name, db_pwd)
        id_covid.createDB()
        id_covid.addCollections()
    else:
        print("Unable to find path")
