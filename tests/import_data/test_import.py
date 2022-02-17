from covidVisualizationTool.imports.importData import ImportData
from common_utilities import get_file_from_path


def test_load_tables(test_db_location):
    test_csv_file = get_file_from_path('../docs/owid-covid-data-2-14-2022.csv', __file__)
    LD = ImportData(db_location=test_db_location, csv_file=test_csv_file)

    assert LD.load_tables()

