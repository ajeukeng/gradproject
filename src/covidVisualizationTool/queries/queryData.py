import pandas as pd

from covidVisualizationTool.imports.base import dbBase
from covidVisualizationTool.imports.models import *


class QueryData(dbBase):
    def __init__(self, db_location):
        super().__init__(db_location)
        self.db_location = db_location

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
        pass

    def get_median_age_death_rate(self):
        """Query to retrieve number median age vs number of deaths over time"""
        pass

    def get_positive_rate_for_total_test(self):
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