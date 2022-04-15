
import click
from covidVisualizationTool.imports.importData import ImportData as ID
import common_utilities as cu
from covidVisualizationTool.queries.queryData import QueryData as QD
from covidVisualizationTool.imports.scrapeData import ScrapeData as SD


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
        query_covid_data = QD(db_location=db_name)
        query_covid_data.get_death_rate_fully_vaccinated()
        query_covid_data.get_median_age_death_rate()
        query_covid_data.get_positive_rate_for_total_tests()
        query_covid_data.get_icu_patients_vaccinations()
        query_covid_data.get_boosted_positive_rate()
        query_covid_data.get_population_vaccinated()
        query_covid_data.get_stringency_death_rate()
    else:
        print("Unable to find database")


@cvt.command()
def get_data():
    scrape_data = SD()
    scrape_data.get_covid_data()


@cvt.command()
def automated_import():
    scrape_data = SD()
    csv_filename = scrape_data.csv_filename
    db_name = scrape_data.db_name
    # Import Covid Dataset directly from new data
    scrape_data.get_covid_data()
    if cu.check_path(csv_filename):
        id_covid = ID(csv_filename, db_name)
        id_covid.load_tables()

    else:
        print("Unable to find path")
