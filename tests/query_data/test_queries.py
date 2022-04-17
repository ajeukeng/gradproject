from covidVisualizationTool.app.common_utilities import get_file_from_path
from covidVisualizationTool.queries.queryData import QueryData

db_location = get_file_from_path('../docs/cvt-2-25-2022.db', __file__)
qd = QueryData(db_location)


def test_simple_query():
    # Simple queries to test functionality. DB will need to be updated.
    all_data = qd.get_all_data()

    assert len(all_data) == 238


def test_deaths_vaccinated():
    # Testing the number of deaths vs number of people vaccinated
    vaccinated_deaths = qd.get_death_rate_fully_vaccinated()
    assert not vaccinated_deaths.empty

    assert vaccinated_deaths.columns.tolist() == ['new_deaths_smoothed',
                                                  'people_vaccinated_per_hundred',
                                                  'new_vaccinations_smoothed_per_million',
                                                  'total_boosters_per_hundred',
                                                  'date',
                                                  'location']


def test_median_age_total_deaths():
    # Testing the number of deaths vs the median age
    median_age_total_deaths = qd.get_median_age_death_rate()
    assert not median_age_total_deaths.empty

    assert median_age_total_deaths.columns.tolist() == ['median_age',
                                                        'total_deaths_per_million',
                                                        'location']


def test_positive_rate_for_total_tests():
    # Testing if the positivity rate increases with the total number of tests
    positive_rate_for_total_tests = qd.get_positive_rate_for_total_tests()
    assert not positive_rate_for_total_tests.empty

    assert positive_rate_for_total_tests.columns.tolist() == ['positive_rate',
                                                              'new_tests_smoothed',
                                                              'date',
                                                              'location']


def test_icu_patients_vaccinations():
    # Testing if the number of icu patients decreases with the number of vaccinations administered
    icu_patients_vaccinations = qd.get_icu_patients_vaccinations()

    assert not icu_patients_vaccinations.empty

    assert icu_patients_vaccinations.columns.tolist() == ['icu_patients_per_million',
                                                          'new_vaccinations_smoothed_per_million',
                                                          'date',
                                                          'location']


def test_boosted_positive_rate():
    # Testing if the positivity rate decreases with more people getting boosted
    boosted_positive_rate = qd.get_boosted_positive_rate()

    assert not boosted_positive_rate.empty

    assert boosted_positive_rate.columns.tolist() == ['total_boosters_per_hundred',
                                                      'new_vaccinations_smoothed_per_million',
                                                      'positive_rate',
                                                      'date',
                                                      'location']


def test_population_vaccinated():
    # Testing if a higher population means fewer people get vaccinated
    population_vaccinated = qd.get_population_vaccinated()
    assert not population_vaccinated.empty

    assert population_vaccinated.columns.tolist() == ['population',
                                                      'total_vaccinations_per_hundred',
                                                      'location']


def test_get_stringency_index():
    # Testing if more stringency meant fewer deaths and cases

    stringency_death_rate = qd.get_stringency_death_rate()

    assert not stringency_death_rate.empty

    assert stringency_death_rate.columns.tolist() == ['total_deaths_per_million',
                                                      'stringency_index',
                                                      'total_cases_per_million',
                                                      'date',
                                                      'location']
