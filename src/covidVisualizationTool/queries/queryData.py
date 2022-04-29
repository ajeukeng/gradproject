import pandas as pd

from covidVisualizationTool.imports.base import dbBase
from covidVisualizationTool.imports.models import *


class QueryData(dbBase):
    def __init__(self, db_location):
        super().__init__(db_location)
        self.db_location = db_location
        self.last_row_median_age_dict = {}
        self.average_positivity_rate_dict = {}
        self.population_density = None
        self.last_row_population_total_vaccinations_dict = {}

    def get_all_data(self):
        """Query to retrieve all distinct artifacts"""
        all_data = self.session.query(Location.location).distinct()
        all_data_list = []
        for data in all_data:
            all_data_list.append(data)

        return all_data_list

    def get_death_rate_fully_vaccinated(self):
        """Query to retrieve the death rate vs number of partially vaccinated individuals over time and boosted"""
        death_rate_fully_vaccinated_query = self.session.query(Deaths.new_deaths_smoothed,
                                                               Vaccinated.people_vaccinated_per_hundred,
                                                               Vaccinated.new_vaccinations_smoothed_per_million,
                                                               Boosted.total_boosters_per_hundred,
                                                               Date.date, Location.location). \
            join(Vaccinated, Deaths.death_vaccination_id == Vaccinated.vaccinated_id). \
            join(Date, Date.date_id == Location.location_date_id). \
            join(Boosted, Boosted.boosted_id == Location.location_boosted_id). \
            join(Location, Vaccinated.vaccinated_id == Location.location_vaccinated_id). \
            filter(Location.location.like('United States')).distinct()
        df = pd.read_sql(death_rate_fully_vaccinated_query.statement,
                         con=self.session.bind)

        # Removes all Nans
        death_rate_fully_vaccinated_df = df.dropna()

        # Reset Index
        death_rate_fully_vaccinated_df = death_rate_fully_vaccinated_df.reset_index(drop=True)

        return death_rate_fully_vaccinated_df


    def get_median_age_death_rate(self):
        """Query to retrieve number median age vs total number of deaths"""
        median_age_death_rate_query = self.session.query(Age.median_age, Deaths.total_deaths_per_million,
                                                         Location.location). \
            join(Deaths, Deaths.deaths_id == Age.age_deaths_id). \
            join(Location, Location.location_age_id == Age.age_id).distinct()
        df = pd.read_sql(median_age_death_rate_query.statement, con=self.session.bind)
        # Verifying dataframe is not empty
        df = df.dropna()

        # Gets the last row of each location based on date and resets index
        median_age_death_rate_df = df.drop_duplicates(subset='location', keep='last', ignore_index=True)

        # Sorts by median age
        median_age_death_rate_df = median_age_death_rate_df.sort_values('total_deaths_per_million')

        return median_age_death_rate_df

    def get_positive_rate_for_total_tests(self):
        """Query to retrieve the number of positive tests vs total tests"""
        positive_rate_for_total_tests_query = self.session.query(Positive.positive_rate, Tests.new_tests_smoothed,
                                                                 Date.date,
                                                                 Location.location). \
            join(Tests, Tests.tests_id == Positive.tests_positive_id). \
            join(Date, Date.date_positive_id == Positive.positive_id). \
            join(Location, Location.location_positive_id == Positive.positive_id). \
            filter(Location.location.like('United States')).distinct()
        df = pd.read_sql(positive_rate_for_total_tests_query.statement,
                         con=self.session.bind)

        # Verifying dataframe is not empty
        positive_rate_for_total_tests_df = df.dropna()

        return positive_rate_for_total_tests_df

    def get_icu_patients_vaccinations(self):
        """Query to retrieve the number of icu patients vs total vaccinations over time"""
        icu_patients_vaccinations_query = self.session.query(ICU.icu_patients_per_million,
                                                             Vaccinated.new_vaccinations_smoothed_per_million,
                                                             Date.date, Location.location). \
            join(ICU, ICU.vaccinated_icu_id == Vaccinated.vaccinated_id). \
            join(Date, Vaccinated.vaccinated_id == Date.date_vaccinated_id). \
            join(Location, Vaccinated.vaccinated_id == Location.location_vaccinated_id). \
            filter(Location.location.like('United States')).distinct()
        df = pd.read_sql(icu_patients_vaccinations_query.statement,
                         con=self.session.bind)

        icu_patients_vaccinations_df = df.dropna()

        return icu_patients_vaccinations_df

    def get_boosted_positive_rate(self):
        """Query to retrieve the number of boosted vs positivity rate over time"""
        boosted_positive_rate_query = self.session.query(Boosted.total_boosters_per_hundred,
                                                         Vaccinated.new_vaccinations_smoothed_per_million,
                                                         Positive.positive_rate,
                                                         Date.date, Location.location). \
            join(Boosted, Boosted.boosted_id == Location.location_boosted_id). \
            join(Positive, Positive.positive_id == Boosted.boosted_positive_id). \
            join(Date, Date.date_positive_id == Positive.positive_id). \
            join(Vaccinated, Vaccinated.vaccinated_id == Location.location_vaccinated_id). \
            filter(Location.location.like('United States')).distinct()
        df = pd.read_sql(boosted_positive_rate_query.statement,
                         con=self.session.bind)

        boosted_positive_rate_df = df.dropna()

        return boosted_positive_rate_df

    def get_population_vaccinated(self):
        """Query to retrieve the correlation between population and likelihood to get vaccinated"""
        population_vaccinated_query = self.session.query(Population.population,
                                                         Vaccinated.total_vaccinations_per_hundred,
                                                         Date.date, Location.location). \
            join(Population, Population.population_vaccination_id == Vaccinated.vaccinated_id). \
            join(Date, Date.date_id == Location.location_date_id). \
            join(Location, Vaccinated.vaccinated_id == Location.location_vaccinated_id).distinct()
        df = pd.read_sql(population_vaccinated_query.statement,
                         con=self.session.bind)

        df = df.dropna()

        # Gets the last row of each location based on date and resets index
        population_vaccinated_df = df.drop_duplicates(subset='location', keep='last', ignore_index=True)

        # Drop date column
        population_vaccinated_df.drop('date', axis=1, inplace=True)

        # Ordered by population
        population_vaccinated_df = population_vaccinated_df.sort_values('population',
                                                                        ascending=False)

        # Removing outliers
        population_vaccinated_df = population_vaccinated_df[10:]

        return population_vaccinated_df

    def get_stringency_death_rate(self):
        """Query to determine if lockdowns helped keep deaths down"""
        stringency_death_rate_query = self.session.query(Deaths.total_deaths_per_million,
                                                         Stringency.stringency_index,
                                                         Cases.total_cases_per_million,
                                                         Date.date,
                                                         Location.location). \
            join(Location, Location.location_deaths_id == Deaths.deaths_id). \
            join(Stringency, Stringency.stringency_id == Location.location_stringency_id). \
            join(Date, Date.date_stringency_id == Stringency.stringency_id). \
            join(Cases, Cases.cases_id == Location.location_cases_id).distinct()
        df = pd.read_sql(stringency_death_rate_query.statement,
                         con=self.session.bind)

        stringency_death_rate_df = df.dropna()

        stringency_death_rate_df.groupby(['location'])['stringency_index'].max()

        # Makes total_deaths_per_million and total_cases_per_million whole numbers
        stringency_death_rate_df.total_deaths_per_million = stringency_death_rate_df.total_deaths_per_million.round()

        # Gets the last row of each location based on date and resets index
        stringency_death_rate_df = stringency_death_rate_df.drop_duplicates(subset='location', keep='last',
                                                                            ignore_index=True)

        print(stringency_death_rate_df)
        return stringency_death_rate_df
