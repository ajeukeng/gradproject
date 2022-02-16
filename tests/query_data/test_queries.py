from common_utilities import get_file_from_path
from covidVisualizationTool.imports.models import Population, Positive, Location
from covidVisualizationTool.queries.queryData import QueryData
import pandas as pd

db_location = get_file_from_path('../docs/cvt-test.db', __file__)
qd = QueryData(db_location)


def test_simple_query():
    # Simple queries to test functionality. DB will need to be updated.
    all_data = qd.get_all_data()

    assert len(all_data) == 238


def test_deaths_vaccinated():
    # Testing the number of deaths vs number of people vaccinated
    vaccinated_deaths = qd.get_death_rate_fully_vaccinated()
    assert vaccinated_deaths.shape == (748, 4)


def test_positive_rate_by_population_density():
    # Testing whether the positivity rate is higher with a higher population density
    positive_rate_by_population_query = qd.session.query(Population.population_density, Positive.positive_rate,
                                                         Location.location). \
        join(Location, Location.location_population_id == Population.population_id). \
        join(Positive, Positive.positive_id == Location.location_positive_id). \
        filter(Location.location.like('United States')).distinct()
    df = pd.read_sql(positive_rate_by_population_query.statement, con=qd.session.bind)
    df = df.dropna()
    assert round(df['positive_rate'].mean(), 6) == 0.125963

    positive_rate_by_population_density = qd.get_positive_rate_by_population_density()

    assert positive_rate_by_population_density.shape == (138, 3)


def test_median_age_total_deaths():
    # Testing the number of deaths vs the median age
    median_age_total_deaths = qd.get_median_age_death_rate()
    assert median_age_total_deaths.shape == (185, 3)
