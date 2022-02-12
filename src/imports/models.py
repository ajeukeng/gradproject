from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
meta = MetaData()


class Location(Base):
    __tablename__ = 'location'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column('location', String(100), nullable=False)
    continent = Column('continent', String(100), nullable=False)
    location_cases_id = Column(Integer, ForeignKey('cases.cases_id'))
    location_tests_id = Column(Integer, ForeignKey('tests.tests_id'))
    location_deaths_id = Column(Integer, ForeignKey('deaths.deaths_id'))
    location_population_id = Column(Integer, ForeignKey('population.population_id'))
    location_date_id = Column(Integer, ForeignKey('date.date_id'))
    location_age_id = Column(Integer, ForeignKey('age.age_id'))
    location_vaccinated_id = Column(Integer, ForeignKey('vaccinated.vaccinated_id'))
    location_icu_id = Column(Integer, ForeignKey('icu.icu_id'))
    location_hospital_id = Column(Integer, ForeignKey('hospital.hospital_id'))
    location_positive_id = Column(Integer, ForeignKey('positive.positive_id'))
    location_boosted_id = Column(Integer, ForeignKey('boosted.boosted_id'))

    def __init__(self, location_id, location, continent, location_cases_id, location_tests_id, location_deaths_id,
                 location_population_id, location_date_id, location_age_id, location_vaccinated_id, location_icu_id,
                 location_hospital_id, location_positive_id, location_boosted_id):
        self.location_id = location_id
        self.location = location
        self.continent = continent
        self.location_cases_id = location_cases_id
        self.location_tests_id = location_tests_id
        self.location_deaths_id = location_deaths_id
        self.location_population_id = location_population_id
        self.location_date_id = location_date_id
        self.location_age_id = location_age_id
        self.location_vaccinated_id = location_vaccinated_id
        self.location_icu_id = location_icu_id
        self.location_hospital_id = location_hospital_id
        self.location_positive_id = location_positive_id
        self.location_boosted_id = location_boosted_id


class Cases(Base):
    __tablename__ = 'cases'
    cases_id = Column(Integer, primary_key=True, autoincrement=True)
    total_cases = Column('total_cases', Integer, nullable=False)
    new_cases = Column('new_cases', Integer, nullable=False)
    new_cases_smoothed = Column('new_cases_smoothed', Integer, nullable=False)
    total_cases_per_million = Column('total_cases_per_million', Integer, nullable=False)
    new_cases_per_million = Column('new_cases_per_million', Integer, nullable=False)
    new_cases_smoothed_per_million = Column('new_cases_smoothed_per_million', Integer, nullable=False)

    def __init__(self, total_cases, new_cases, new_cases_smoothed, total_cases_per_million, new_cases_per_million,
                 new_cases_smoothed_per_millino):
        self.total_cases = total_cases
        self.new_cases = new_cases
        self.new_cases_smoothed = new_cases_smoothed
        self.total_cases_per_million = total_cases_per_million
        self.new_cases_per_million = new_cases_per_million
        self.new_cases_smoothed_per_million = new_cases_smoothed_per_millino


class Tests(Base):
    __tablename__ = 'tests'
    tests_id = Column(Integer, primary_key=True, autoincrement=True)
    new_tests = Column('new_tests', Integer, nullable=False)
    total_tests = Column('total_tests', Integer, nullable=False)
    total_tests_per_thousand = Column('total_tests_per_thousand', Integer, nullable=False)
    new_tests_per_thousand = Column('new_tests_per_thousand', Integer, nullable=False)
    new_tests_smoothed = Column('new_tests_smoothed', Integer, nullable=False)
    new_tests_smoothed_per_thousand = Column('new_tests_smoothed_per_thousand', Integer, nullable=False)
    tests_per_case = Column('tests_per_case', Integer, nullable=False)
    test_units = Column('test_units', Integer, nullable=False)

    def __init__(self, new_tests, total_tests, total_tests_per_thousand, new_tests_per_thousand, new_tests_smoothed,
                 new_tests_smoothed_per_thousand, tests_per_case, test_units):
        self.new_tests = new_tests
        self.total_tests = total_tests
        self.total_tests_per_thousand = total_tests_per_thousand
        self.new_tests_per_thousand = new_tests_per_thousand
        self.new_tests_smoothed = new_tests_smoothed
        self.new_tests_smoothed_per_thousand = new_tests_smoothed_per_thousand
        self.tests_per_case = tests_per_case
        self.test_units = test_units


class Deaths(Base):
    __tablename__ = 'deaths'
    deaths_id = Column(Integer, primary_key=True, autoincrement=True)
    total_deaths = Column('total_deaths', Integer, nullable=False)
    new_deaths = Column('new_deaths', Integer, nullable=False)
    new_deaths_smoothed = Column('new_deaths_smoothed', Integer, nullable=False)
    total_deaths_per_million = Column('total_deaths_per_million', Integer, nullable=False)
    new_deaths_per_million = Column('new_deaths_per_million', Integer, nullable=False)
    new_deaths_smoothed_per_million = Column('new_deaths_smoothed_per_million', Integer, nullable=False)
    death_vaccination_id = Column(Integer, ForeignKey('vaccinated.vaccinated_id'))

    def __init__(self, total_deaths, new_deaths, new_deaths_smoothed, total_deaths_per_million,
                 new_deaths_per_million, new_deaths_smoothed_per_million, death_vaccination_id):
        self.total_deaths = total_deaths
        self.new_deaths = new_deaths
        self.new_deaths_smoothed = new_deaths_smoothed
        self.total_deaths_per_million = total_deaths_per_million
        self.new_deaths_per_million = new_deaths_per_million
        self.new_deaths_smoothed_per_million = new_deaths_smoothed_per_million
        self.death_vaccination_id = death_vaccination_id


class Population(Base):
    __tablename__ = 'population'
    population_id = Column(Integer, primary_key=True, autoincrement=True)
    population = Column('population', Integer, nullable=False)
    population_density = Column('population_density', Integer, nullable=False)
    population_cases_id = Column(Integer, ForeignKey('cases.cases_id'))
    population_vaccination_id = Column(Integer, ForeignKey('vaccinated.vaccinated_id'))

    def __init__(self, population, population_density, population_cases_id,
                 population_vaccination_id):
        self.population = population
        self.population_density = population_density
        self.population_cases_id = population_cases_id
        self.population_vaccination_id = population_vaccination_id


class Date(Base):
    __tablename__ = 'date'
    date_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column('date', String(100))

    def __init__(self, date):
        self.date = date


class Age(Base):
    __tablename__ = 'age'
    age_id = Column(Integer, primary_key=True, autoincrement=True)
    median_age = Column('median_age', Integer, nullable=False)
    aged_65_older = Column('aged_65_older', Integer, nullable=False)
    aged_70_older = Column('aged_70_older', Integer, nullable=False)
    age_deaths_id = Column(Integer, ForeignKey('deaths.deaths_id'))

    def __init__(self, median_age, aged_65_older, aged_70_older, age_deaths_id):
        self.median_age = median_age
        self.aged_65_older = aged_65_older
        self.aged_70_older = aged_70_older
        self.age_deaths_id = age_deaths_id


class Vaccinated(Base):
    __tablename__ = 'vaccinated'
    vaccinated_id = Column(Integer, primary_key=True, autoincrement=True)
    total_vaccinations = Column('total_vaccinations', Integer, nullable=True)
    people_vaccinated = Column('people_vaccinated', Integer, nullable=True)
    people_fully_vaccinated = Column('people_fully_vaccinated', Integer, nullable=True)
    new_vaccinations = Column('new_vaccinations', Integer, nullable=True)
    new_vaccinations_smoothed = Column('new_vaccinations_smoothed', Integer, nullable=True)
    total_vaccinations_per_hundred = Column('total_vaccinations_per_hundred', Integer, nullable=True)
    people_vaccinated_per_hundred = Column('people_vaccinated_per_hundred', Integer, nullable=True)
    people_fully_vaccinated_per_hundred = Column('people_fully_vaccinated_per_hundred', Integer, nullable=True)
    new_vaccinations_smoothed_per_million = Column('new_vaccinations_smoothed_per_million', Integer, nullable=True)
    new_people_vaccinated_smoothed = Column('new_people_vaccinated_smoothed', Integer, nullable=True)

    def __init__(self, scan_tool):
        self.scan_tool = scan_tool


class Boosted(Base):
    __tablename__ = 'boosted'
    boosted_id = Column(Integer, primary_key=True, autoincrement=True)
    total_boosters = Column('total_boosters', Integer, nullable=True)
    total_boosters_per_hundred = Column('total_boosters_per_hundred', Integer, nullable=True)

    def __init__(self, total_boosters, total_boosters_per_hundred):
        self.total_boosters = total_boosters
        self.total_boosters_per_hundred = total_boosters_per_hundred


class ICU(Base):
    __tablename__ = 'icu'
    icu_id = Column(Integer, primary_key=True, nullable=False)
    icu_patients = Column('icu_patients', Integer, nullable=True)
    icu_patients_per_million = Column('icu_patients_per_million', Integer, nullable=True)
    weekly_icu_admissions = Column('weekly_icu_admissions', Integer, nullable=False)
    weekly_icu_admissions_per_million = Column('weekly_icu_admissions_per_million', Integer, nullable=False)
    vaccinated_icu_id = Column(Integer, ForeignKey('vaccinated.vaccinated_id'))

    def __init__(self, icu_patients, icu_patients_per_million, weekly_icu_admissions,
                 weekly_icu_admissions_per_million, vaccinated_icu_id):
        self.icu_patients = icu_patients
        self.icu_patients_per_million = icu_patients_per_million
        self.weekly_icu_admissions = weekly_icu_admissions
        self.weekly_icu_admissions_per_million = weekly_icu_admissions_per_million
        self.vaccinated_icu_id = vaccinated_icu_id


class Hospital(Base):
    __tablename__ = 'hospital'
    hospital_id = Column(Integer, primary_key=True, nullable=False)
    hosp_patients = Column('hosp_patients', Integer, nullable=False)
    hosp_patients_per_million = Column('hosp_patients_per_million', Integer, nullable=False)
    weekly_hosp_admissions = Column('weekly_hosp_admissions', Integer, nullable=False)
    weekly_hosp_admissions_per_million = Column('weekly_hosp_admissions_per_million', Integer, nullable=False)

    def __init__(self, hosp_patients, hosp_patients_per_million,
                 weekly_hosp_admissions, weekly_hosp_admissions_per_million):
        self.hosp_patients = hosp_patients
        self.hosp_patients_per_million = hosp_patients_per_million
        self.weekly_hosp_admissions = weekly_hosp_admissions
        self.weekly_hosp_admissions_per_million = weekly_hosp_admissions_per_million


class Positive(Base):
    __tablename__ = 'positive'
    positive_id = Column(Integer, primary_key=True, nullable=False)
    positive_rate = Column('positive_rate', Integer, nullable=False)
    tests_positive_id = Column(Integer, ForeignKey('tests.tests_id'))

    def __init__(self, positive_rate, tests_positive_id):
        self.positive_rate = positive_rate
        self.tests_positive_id = tests_positive_id
