import datetime

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

    def get_all_data(self):
        """Query to retrieve all distinct artifacts"""
        all_data = self.session.query(Location.location).distinct()
        all_data_list = []
        for data in all_data:
            all_data_list.append(data)

        return all_data_list

    def get_death_rate_fully_vaccinated(self):
        """Query to retrieve the death rate vs number of partially vaccinated individuals over time"""
        death_rate_fully_vaccinated_query = self.session.query(Deaths.new_deaths_smoothed_per_million,
                                                               Vaccinated.new_vaccinations_smoothed_per_million,
                                                               Date.date, Location.location). \
            join(Vaccinated, Deaths.death_vaccination_id == Vaccinated.vaccinated_id). \
            join(Date, Date.date_id == Location.location_date_id). \
            join(Location, Vaccinated.vaccinated_id == Location.location_vaccinated_id). \
            filter(Location.location.like('United States')).distinct()
        death_rate_fully_vaccinated_df = pd.read_sql(death_rate_fully_vaccinated_query.statement,
                                                     con=self.session.bind)
        # Replacing all NANs with 0s
        death_rate_fully_vaccinated_df['new_deaths_smoothed_per_million'] = death_rate_fully_vaccinated_df[
            'new_deaths_smoothed_per_million'].fillna(0)
        death_rate_fully_vaccinated_df['new_vaccinations_smoothed_per_million'] = death_rate_fully_vaccinated_df[
            'new_vaccinations_smoothed_per_million'].fillna(0)

        # Remove dates prior to when people started getting vaccinated
        death_rate_fully_vaccinated_df['date'] = pd.to_datetime(death_rate_fully_vaccinated_df['date'],
                                                                format='%Y-%m-%d')
        death_rate_fully_vaccinated_df = death_rate_fully_vaccinated_df.loc[(death_rate_fully_vaccinated_df['date'] >=
                                                                             '2020-12-13')]
        # Converts date field back to string instead of datetime
        death_rate_fully_vaccinated_df['date'] = death_rate_fully_vaccinated_df['date'].astype('string')

        # TODO: Could be used for logging
        print(death_rate_fully_vaccinated_df)

        return death_rate_fully_vaccinated_df

    def get_death_rate_partially_vaccinated(self):
        """Query to retrieve the death rate vs number of partially vaccinated individuals over time"""
        pass

    def get_positive_rate_by_population_density(self):
        """Query to retrieve positivity rate based on population density over time"""
        positive_rate_by_population_query = self.session.query(Population.population_density, Positive.positive_rate,
                                                               Location.location). \
            join(Location, Location.location_population_id == Population.population_id). \
            join(Positive, Positive.positive_id == Location.location_positive_id).distinct()
        df = pd.read_sql(positive_rate_by_population_query.statement, con=self.session.bind)
        df = df.dropna()

        all_locations = df['location'].unique()
        positive_rate_by_population_df = pd.DataFrame()
        # Counter for the number of positive_rate data points
        counter = 0
        positive_rate = 0

        for location in all_locations:
            for index in df.index:
                if df['location'][index] == location:
                    positive_rate += df['positive_rate'][index]
                    self.population_density = df['population_density'][index]
                    counter += 1
            # Gets the average positive_rate for each country
            self.average_positivity_rate_dict = {'population_density': self.population_density,
                                                 'average_positive_rate': positive_rate/counter,
                                                 'location': location}
            counter = 0
            positive_rate = 0
            df2 = pd.DataFrame([self.average_positivity_rate_dict])
            positive_rate_by_population_df = pd.concat([positive_rate_by_population_df, df2], ignore_index=True)

        # TODO: Could be used for logging
        print(positive_rate_by_population_df)

        return positive_rate_by_population_df

    def get_median_age_death_rate(self):
        """Query to retrieve number median age vs number of deaths over time"""
        median_age_death_rate_query = self.session.query(Age.median_age, Deaths.total_deaths, Location.location). \
            join(Deaths, Deaths.deaths_id == Age.age_deaths_id). \
            join(Location, Location.location_age_id == Age.age_id).distinct()
        df = pd.read_sql(median_age_death_rate_query.statement, con=self.session.bind)
        all_locations = df['location'].unique()
        median_age_death_rate_df = pd.DataFrame(columns=['median_age', 'total_deaths', 'location'])

        # Loops through all the location (aka countries) then checks total deaths for that country and
        # takes the last total deaths which is the largest
        for location in all_locations:
            for index in df.index:
                if df['location'][index] == location:
                    dict_row = {'median_age': df['median_age'][index], 'total_deaths': df['total_deaths'][index],
                                'location': df['location'][index]}
                    self.last_row_median_age_dict = dict_row

            df2 = pd.DataFrame([self.last_row_median_age_dict])
            median_age_death_rate_df = pd.concat([median_age_death_rate_df, df2], ignore_index=True)

        median_age_death_rate_df = median_age_death_rate_df.dropna()
        print(median_age_death_rate_df)

        return median_age_death_rate_df

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
