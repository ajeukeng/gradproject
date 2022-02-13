from covidVisualizationTool.imports.importData import ImportData
from common_utilities import get_file_from_path
from covidVisualizationTool.queries.queryData import QueryData


def test_load_tables(test_db_location):
    test_csv_file = get_file_from_path('../docs/owid-covid-data.csv', __file__)
    LD = ImportData(db_location=test_db_location, csv_file=test_csv_file)

    assert LD.load_tables()

