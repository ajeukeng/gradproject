import sqlite3

from covidVisualizationTool.imports.base import dbBase
import pandas as pd

from covidVisualizationTool.imports.models import *


class ImportData(dbBase):
    """ Inserts data into database ensuring there are not duplicates"""

    def __init__(self, csv_file, db_location):
        super().__init__(db_location)
        self.db_location = db_location
        self.csv_file = csv_file
        Base.metadata.create_all(self.engine)
        self.id_count = 1

    def load_tables(self):
        """load tables with data"""
        df = pd.read_csv(self.csv_file)
        for index, row in df.iterrows():
            cases = Cases(total_cases=row['total_cases'], new_cases=row['new_cases'],
                          new_cases_smoothed=row['new_cases_smoothed'],
                          total_cases_per_million=row['total_cases_per_million'],
                          new_cases_per_million=row['new_cases_per_million'],
                          new_cases_smoothed_per_million=row['new_cases_smoothed_per_million'])

            self.add_new_row(cases)

            tests = Tests(new_tests=row['new_tests'], total_tests=row['total_tests'],
                          total_tests_per_thousand=row['total_tests_per_thousand'],
                          new_tests_per_thousand=row['new_tests_per_thousand'],
                          new_tests_smoothed=row['new_tests_smoothed'],
                          new_tests_smoothed_per_thousand=row['new_tests_smoothed_per_thousand'],
                          tests_per_case=row['tests_per_case'])

            self.add_new_row(tests)

            vaccinated = Vaccinated(total_vaccinations=row['total_vaccinations'],
                                    people_vaccinated=row['people_vaccinated'],
                                    people_fully_vaccinated=row['people_fully_vaccinated'],
                                    new_vaccinations=row['new_vaccinations'],
                                    new_vaccinations_smoothed=row['new_vaccinations_smoothed'],
                                    total_vaccinations_per_hundred=row['total_vaccinations_per_hundred'],
                                    people_vaccinated_per_hundred=row['people_vaccinated_per_hundred'],
                                    people_fully_vaccinated_per_hundred=row['people_fully_vaccinated_per_hundred'],
                                    new_vaccinations_smoothed_per_million=row['new_vaccinations_smoothed_per_million'],
                                    new_people_vaccinated_smoothed=row['new_people_vaccinated_smoothed'])
            self.add_new_row(vaccinated)

            deaths = Deaths(total_deaths=row['total_deaths'], new_deaths=row['new_deaths'],
                            new_deaths_smoothed=row['new_deaths_smoothed'],
                            total_deaths_per_million=row['total_deaths_per_million'],
                            new_deaths_per_million=row['new_deaths_per_million'],
                            new_deaths_smoothed_per_million=row['new_deaths_smoothed_per_million'],
                            death_vaccination_id=vaccinated.vaccinated_id)

            self.add_new_row(deaths)

            population = Population(population=row['population'], population_density=row['population_density'],
                                    population_cases_id=cases.cases_id,
                                    population_vaccination_id=vaccinated.vaccinated_id)

            self.add_new_row(population)

            age = Age(median_age=row['median_age'], aged_65_older=row['aged_65_older'],
                      aged_70_older=row['aged_70_older'], age_deaths_id=deaths.deaths_id)

            self.add_new_row(age)

            icu = ICU(icu_patients=row['icu_patients'], icu_patients_per_million=row['icu_patients_per_million'],
                      weekly_icu_admissions=row['weekly_icu_admissions'],
                      weekly_icu_admissions_per_million=row['weekly_icu_admissions_per_million'],
                      vaccinated_icu_id=vaccinated.vaccinated_id)

            self.add_new_row(icu)

            hospital = Hospital(hosp_patients=row['hosp_patients'],
                                hosp_patients_per_million=row['hosp_patients_per_million'],
                                weekly_hosp_admissions=row['weekly_hosp_admissions'],
                                weekly_hosp_admissions_per_million=row['weekly_hosp_admissions_per_million'])

            self.add_new_row(hospital)

            positive = Positive(positive_rate=row['positive_rate'], tests_positive_id=tests.tests_id)

            self.add_new_row(positive)

            boosted = Boosted(total_boosters=row['total_boosters'],
                              total_boosters_per_hundred=row['total_boosters_per_hundred'],
                              boosted_positive_id=positive.positive_id)
            self.add_new_row(boosted)

            stringency = Stringency(stringency_index=row['stringency_index'], stringency_deaths_id=deaths.deaths_id)
            self.add_new_row(stringency)

            date = Date(date=row['date'], date_positive_id=positive.positive_id,
                        date_vaccinated_id=vaccinated.vaccinated_id, date_deaths_id=deaths.deaths_id,
                        date_stringency_id=stringency.stringency_id)
            self.add_new_row(date)

            location = Location(location=row['location'], continent=row['continent'], location_cases_id=cases.cases_id,
                                location_tests_id=tests.tests_id, location_deaths_id=deaths.deaths_id,
                                location_population_id=population.population_id, location_date_id=date.date_id,
                                location_age_id=age.age_id, location_vaccinated_id=vaccinated.vaccinated_id,
                                location_icu_id=icu.icu_id, location_hospital_id=hospital.hospital_id,
                                location_positive_id=positive.positive_id, location_boosted_id=boosted.boosted_id,
                                location_stringency_id=stringency.stringency_index)

            self.add_new_row(location)

            self.id_count = self.id_count + 1

        self.session.close()

    def add_new_row(self, new_row):
        """Adds new row to database"""
        try:
            self.session.add(new_row)
            self.session.commit()
            self.session.flush()
        except sqlite3.IntegrityError as e:
            print(e)
        except Exception as e:
            self.session.rollback()
            print(e)
            return False
        return True
