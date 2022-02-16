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
        id_covid = ID(csv_location, db_name)
        id_covid.load_tables()
    else:
        print("Unable to find path")


@cvt.command()
@click.argument('db_name')
def query_data(db_name: str):
    if cu.check_path(db_name):
        query_stuff = QD(db_location=db_name)
        query_stuff.get_death_rate_partially_vaccinated()
        query_stuff.get_positive_rate_by_population_density()
        query_stuff.get_median_age_death_rate()
    else:
        print("Unable to find database")
