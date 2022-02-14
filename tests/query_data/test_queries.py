from common_utilities import get_file_from_path
from covidVisualizationTool.queries.queryData import QueryData
import pandas as pd

db_location = get_file_from_path('../docs/test_db.db', __file__)
qd = QueryData(db_location)


def test_simple_query():
    # Simple queries to test functionality. DB will need to be updated.
    all_data = qd.get_all_data()

    assert len(all_data) == 238


def test_deaths_vaccinated():
    # Testing the number of deaths vs number of people vaccinated
    vaccinated_deaths = qd.get_death_rate_partially_vaccinated()
    df = pd.read_sql(vaccinated_deaths.statement, con=qd.session.bind)
    assert df.shape == (748, 4)
