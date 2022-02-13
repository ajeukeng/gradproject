from common_utilities import get_file_from_path
from covidVisualizationTool.queries.queryData import QueryData


def test_simple_query():
    # Simple queries to test functionality. DB will need to be updated.
    db_location = get_file_from_path('../docs/test_db.db', __file__)
    all_data = QueryData(db_location).get_all_data()

    assert len(all_data) == 238