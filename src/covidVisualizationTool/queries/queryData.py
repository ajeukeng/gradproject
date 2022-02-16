import pandas as pd

from covidVisualizationTool.imports.base import dbBase
from covidVisualizationTool.imports.models import *


class QueryData(dbBase):
    def __init__(self, db_location):
        super().__init__(db_location)
        self.db_location = db_location
        self.last_row_median_age_dict = {}

    def get_all_data(self):
        """Query to retrieve all distinct artifacts"""
        all_data = self.session.query(Location.location).distinct()
        all_data_list = []
        for data in all_data:
            all_data_list.append(data)

        return all_data_list

    def get_death_rate_partially_vaccinated(self):
        """Query to retrieve the death rate vs number of partially vaccinated individuals over time"""
        death_rate_partially_vaccinated_query = self.session.query(Deaths.new_deaths_smoothed_per_million, Vaccinated.new_vaccinations_smoothed_per_million,
                                                                   Date.date, Location.location).\
            join(Vaccinated, Deaths.death_vaccination_id == Vaccinated.vaccinated_id).\
            join(Date, Date.date_id == Location.location_date_id).\
            join(Location, Vaccinated.vaccinated_id == Location.location_vaccinated_id).\
            filter(Location.location.like('United States')).distinct()
        # TODO: Could be used for logging
        df = pd.read_sql(death_rate_partially_vaccinated_query.statement, con=self.session.bind)
        print(df)

        return death_rate_partially_vaccinated_query

    def get_death_rate_fully_vaccinated(self):
        """Query to retrieve the death rate vs number of fully vaccinated individuals over time"""
        pass

    def get_positive_rate_by_population_density(self):
        """Query to retrieve positivity rate based on population density over time"""
        positive_rate_by_population_query = self.session.query(Population.population_density, Positive.positive_rate,
                                                               Location.location). \
            join(Location, Location.location_population_id == Population.population_id). \
            join(Positive, Positive.positive_id == Location.location_positive_id).distinct()
        # TODO: Could be used for logging
        df = pd.read_sql(positive_rate_by_population_query.statement, con=self.session.bind)
        print(df)

        return positive_rate_by_population_query

    def get_median_age_death_rate(self):
        """Query to retrieve number median age vs number of deaths over time"""
        median_age_death_rate_query = self.session.query(Age.median_age, Deaths.total_deaths, Location.location). \
            join(Deaths, Deaths.deaths_id == Age.age_deaths_id). \
            join(Location, Location.location_age_id == Age.age_id).distinct()
        # TODO: Could be used for logging
        df = pd.read_sql(median_age_death_rate_query.statement, con=self.session.bind)
        all_locations = df['location'].unique()
        updated_df = pd.DataFrame(columns=['median_age', 'total_deaths', 'location'])

        for location in all_locations:
            for index in df.index:
                if df['location'][index] == location:
                    dict_row = {'median_age': df['median_age'][index], 'total_deaths': df['total_deaths'][index],
                                'location': df['location'][index]}
                    print(dict_row)
                    self.last_row_median_age_dict = dict_row

            df2 = pd.DataFrame([self.last_row_median_age_dict])
            updated_df = pd.concat([updated_df, df2], ignore_index=True)

        print(updated_df)

        return median_age_death_rate_query

    def get_positive_rate_for_total_tests(self):
        """Query to retrieve the number of positive tests vs total tests"""
        pass

    def get_icu_patients_vaccinations(self):
        """Query to retrieve the number of icu patients vs total vaccinations over time"""
        pass

    def get_boosted_positive_rate(self):
        """Query to retrieve the number of boosted vs positivity rate over time"""
        pass

    def get_population_vaccinated(self):
        """Query to retrieve the correlation between population and likelihood to get vaccinated"""
        pass