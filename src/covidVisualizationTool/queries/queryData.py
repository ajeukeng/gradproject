import pandas as pd

from covidVisualizationTool.imports.base import dbBase
from covidVisualizationTool.imports.models import *
from common_utilities import CommonUtilities as cu


class QueryData(dbBase):
    def __init__(self, db_location):
        super().__init__(db_location)
        self.db_location = db_location
        self.last_row_median_age_dict = {}
        self.average_positivity_rate_dict = {}
        self.population_density = None
        self.last_row_population_total_vaccinations_dict = {}
        self.cvt_logger = cu().cvt_logger()

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
        # Verifying df is not empty
        if df.empty:
            self.cvt_logger.error("Death rate vs Vaccinated dataframe is empty")

        # Removes all Nans
        death_rate_fully_vaccinated_df = df.dropna()

        # Reset Index
        death_rate_fully_vaccinated_df = death_rate_fully_vaccinated_df.reset_index(drop=True)

        self.cvt_logger.info('Partially Vaccinated, Fully Vaccinated, and Boosted vs New Deaths\n')
        self.cvt_logger.info(death_rate_fully_vaccinated_df)

        return death_rate_fully_vaccinated_df

    def get_positive_rate_by_population_density(self):
        """Query to retrieve positivity rate based on population density over time"""
        positive_rate_by_population_query = self.session.query(Population.population_density, Positive.positive_rate,
                                                               Date.date,
                                                               Location.location). \
            join(Location, Location.location_population_id == Population.population_id). \
            join(Positive, Positive.positive_id == Location.location_positive_id). \
            join(Date, Date.date_positive_id == Positive.positive_id).distinct()
        df = pd.read_sql(positive_rate_by_population_query.statement, con=self.session.bind)

        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("Positive Rate by Population Density dataframe is empty")
        df = df.dropna()
        positive_rate_by_population_df = pd.DataFrame(columns=['population_density', 'average_positive_rate',
                                                               'location'])
        all_locations = df['location'].unique()
        # Used to get most recent positive_rate based on date
        df_w_last_positive_rate = df.drop_duplicates(subset='location', keep='last', ignore_index=True)
        for location in all_locations:
            count_result = df['location'].value_counts()[location]

            # Gets sum of the positive rate of each location
            df_to_get_sum_of_each_positive_rate = df.groupby(['location']).positive_rate.sum().reset_index()
            positive_sum = df_to_get_sum_of_each_positive_rate.loc[df_to_get_sum_of_each_positive_rate['location']
                                                                   == location, 'positive_rate'].iloc[0]

            pop_density = \
                df_w_last_positive_rate.loc[df_w_last_positive_rate['location'] == location, 'population_density'].iloc[
                    0]

            self.average_positivity_rate_dict = {'population_density': pop_density,
                                                 'average_positive_rate': int(positive_sum) / count_result,
                                                 'location': location}

            df2 = pd.DataFrame([self.average_positivity_rate_dict])
            positive_rate_by_population_df = pd.concat([positive_rate_by_population_df, df2], ignore_index=True)

        # Ordered by population density
        positive_rate_by_population_df = positive_rate_by_population_df.sort_values('population_density',
                                                                                    ascending=False)

        # Removing outliers
        positive_rate_by_population_df = positive_rate_by_population_df[7:]

        self.cvt_logger.info('Positivity Rate vs Population Density\n')
        self.cvt_logger.info(positive_rate_by_population_df)

        return positive_rate_by_population_df

    def get_median_age_death_rate(self):
        """Query to retrieve number median age vs total number of deaths"""
        median_age_death_rate_query = self.session.query(Age.median_age, Deaths.total_deaths_per_million,
                                                         Location.location). \
            join(Deaths, Deaths.deaths_id == Age.age_deaths_id). \
            join(Location, Location.location_age_id == Age.age_id).distinct()
        df = pd.read_sql(median_age_death_rate_query.statement, con=self.session.bind)
        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("Median Age vs Death Rate dataframe is empty")
        df = df.dropna()

        # Gets the last row of each location based on date and resets index
        median_age_death_rate_df = df.drop_duplicates(subset='location', keep='last', ignore_index=True)

        # Sorts by median age
        median_age_death_rate_df = median_age_death_rate_df.sort_values('total_deaths_per_million')

        self.cvt_logger.info('Median Age vs Death Rate\n')
        self.cvt_logger.info(median_age_death_rate_df)

        return median_age_death_rate_df

    def get_positive_rate_for_total_tests(self):
        """Query to retrieve the number of positive tests vs total tests"""
        positive_rate_for_total_tests_query = self.session.query(Positive.positive_rate, Tests.new_tests_per_thousand,
                                                                 Date.date,
                                                                 Location.location). \
            join(Tests, Tests.tests_id == Positive.tests_positive_id). \
            join(Date, Date.date_positive_id == Positive.positive_id). \
            join(Location, Location.location_positive_id == Positive.positive_id). \
            filter(Location.location.like('United States')).distinct()
        df = pd.read_sql(positive_rate_for_total_tests_query.statement,
                         con=self.session.bind)

        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("Positive Rate vs Total Tests dataframe is empty")
        positive_rate_for_total_tests_df = df.dropna()

        self.cvt_logger.info('Positivity Rate vs Total Tests\n')
        self.cvt_logger.info(positive_rate_for_total_tests_df)

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

        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("ICU patients vs Vaccinations dataframe is empty")

        icu_patients_vaccinations_df = df.dropna()

        self.cvt_logger.info('ICU Patients vs Vaccinations\n')
        self.cvt_logger.info(icu_patients_vaccinations_df)

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

        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("Boosted vs Positive Rate dataframe is empty")

        boosted_positive_rate_df = df.dropna()

        self.cvt_logger.info('Boosted vs Positivity Rate\n')
        self.cvt_logger.info(boosted_positive_rate_df)

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

        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("Population vs Vaccinated dataframe is empty")
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

        self.cvt_logger.info('Population vs Vaccination Rate\n')
        self.cvt_logger.info(population_vaccinated_df)

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

        # Verifying dataframe is not empty
        if df.empty:
            self.cvt_logger.error("Stringency vs Death Rate dataframe is empty")
        stringency_death_rate_df = df.dropna()

        stringency_death_rate_df.groupby(['location'])['stringency_index'].mean()

        # Gets the last row of each location based on date and resets index
        stringency_death_rate_df = stringency_death_rate_df.drop_duplicates(subset='location', keep='last',
                                                                            ignore_index=True)

        self.cvt_logger.info('Stringency vs Death Rate and Cases\n')
        self.cvt_logger.info(stringency_death_rate_df)

        return stringency_death_rate_df
