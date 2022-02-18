from common_utilities import get_file_from_path
from covidVisualizationTool.imports.models import Population, Positive, Location, Date
from covidVisualizationTool.queries.queryData import QueryData
import pandas as pd

db_location = get_file_from_path('../docs/cvt-updated.db', __file__)
qd = QueryData(db_location)


def test_simple_query():
    # Simple queries to test functionality. DB will need to be updated.
    all_data = qd.get_all_data()

    assert len(all_data) == 238


def test_deaths_vaccinated():
    # Testing the number of deaths vs number of people vaccinated
    vaccinated_deaths = qd.get_death_rate_fully_vaccinated()
    assert vaccinated_deaths.shape == (427, 4)


def test_positive_rate_by_population_density():
    # Testing whether the positivity rate is higher with a higher population density
    positive_rate_by_population_query = qd.session.query(Population.population_density, Positive.positive_rate,
                                                         Date.date,
                                                         Location.location). \
        join(Location, Location.location_population_id == Population.population_id). \
        join(Positive, Positive.positive_id == Location.location_positive_id). \
        join(Date, Date.date_positive_id == Positive.positive_id). \
        filter(Location.location.like('United States')).distinct()
    df = pd.read_sql(positive_rate_by_population_query.statement, con=qd.session.bind)
    df = df.dropna()
    assert round(df['positive_rate'].mean(), 3) == 0.088

    assert df['location'].value_counts()['United States'] == 704

    positive_rate_by_population_density = qd.get_positive_rate_by_population_density()

    assert positive_rate_by_population_density.shape == (138, 3)


def test_median_age_total_deaths():
    # Testing the number of deaths vs the median age
    median_age_total_deaths = qd.get_median_age_death_rate()
    assert median_age_total_deaths.shape == (186, 3)


def test_positive_rate_for_total_tests():
    # Testing if the positivity rate increases with the total number of tests
    positive_rate_for_total_tests = qd.get_positive_rate_for_total_tests()
    assert positive_rate_for_total_tests.shape == (704, 4)


def test_icu_patients_vaccinations():
    # Testing if the number of icu patients decreases with the number of vaccinations administered
    icu_patients_vaccinations = qd.get_icu_patients_vaccinations()

    assert icu_patients_vaccinations.shape == (426, 4)


def test_boosted_positive_rate():
    # Testing if the positivity rate decreases with more people getting boosted
    boosted_positive_rate = qd.get_boosted_positive_rate()

    assert boosted_positive_rate.shape == (180, 4)


def test_population_vaccinated():
    # Testing if a higher population means fewer people get vaccinated
    population_vaccinated = qd.get_population_vaccinated()
    assert population_vaccinated.shape == (204, 4)
