from flask import Flask, render_template

from common_utilities import get_file_from_path
from covidVisualizationTool.queries.queryData import QueryData as qd

app = Flask(__name__)
db_location = get_file_from_path('../../../docs/cvt-2-25-2022.db', __file__)
query_data = qd(db_location=db_location)


@app.route("/", methods=("POST", "GET"))
def home():
    return render_template('index.html')


@app.route("/vaccinated_deaths")
def vaccinated_deaths():
    death_rate_fully_vaccinated_df = query_data.get_death_rate_fully_vaccinated()

    vaccinated = death_rate_fully_vaccinated_df['new_vaccinations_smoothed_per_million'].tolist()
    partially_vaccinated = death_rate_fully_vaccinated_df['people_vaccinated_per_hundred'].tolist()
    labels = death_rate_fully_vaccinated_df["date"].tolist()
    deaths = death_rate_fully_vaccinated_df["new_deaths_smoothed"].tolist()
    boosted = death_rate_fully_vaccinated_df["total_boosters_per_hundred"].tolist()

    return render_template('vaccinated_deaths.html', deaths=deaths, labels=labels,
                           vaccinated=vaccinated, boosted=boosted, partially_vaccinated=partially_vaccinated)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/positive_rate_by_population_density")
def positive_rate_by_population_density():
    positive_rate_by_population_density_df = query_data.get_positive_rate_by_population_density()
    countries = positive_rate_by_population_density_df['location'].tolist()
    population_density = positive_rate_by_population_density_df['population_density'].tolist()
    positive_rate = positive_rate_by_population_density_df['average_positive_rate'].tolist()

    return render_template('positive_rate_by_population_density.html', labels=countries,
                           population_density=population_density, positive_rate=positive_rate)


@app.route("/median_age_death_rate")
def median_age_death_rate():
    median_age_death_rate_df = query_data.get_median_age_death_rate()

    age = median_age_death_rate_df['median_age'].tolist()
    deaths = median_age_death_rate_df['total_deaths_per_million'].tolist()
    countries = median_age_death_rate_df['location'].tolist()

    return render_template('median_age_death_rate.html', age=age, deaths=deaths, labels=countries)


@app.route("/positive_rate_for_total_tests")
def positive_rate_for_total_tests():
    positive_rate_for_total_tests_df = query_data.get_positive_rate_for_total_tests()

    positive_rate = positive_rate_for_total_tests_df['positive_rate'].tolist()
    tests = positive_rate_for_total_tests_df['new_tests_per_thousand'].tolist()
    date = positive_rate_for_total_tests_df['date'].tolist()

    return render_template('positive_rate_for_total_tests.html', positive_rate=positive_rate, tests=tests, labels=date)


@app.route("/icu_patients_vaccinations")
def icu_patients_vaccinations():
    icu_patients_vaccinations_df = query_data.get_icu_patients_vaccinations()
    patients = icu_patients_vaccinations_df['icu_patients_per_million'].tolist()
    date = icu_patients_vaccinations_df['date'].tolist()
    vaccinated = icu_patients_vaccinations_df['new_vaccinations_smoothed_per_million'].tolist()

    return render_template('icu_patients_vaccinations.html', labels=date, patients=patients, vaccinated=vaccinated)


@app.route("/boosted_positive_rate")
def boosted_positive_rate():
    boosted_positive_rate_df = query_data.get_boosted_positive_rate()

    boosted = boosted_positive_rate_df['total_boosters_per_hundred'].tolist()
    positive = boosted_positive_rate_df['positive_rate'].tolist()
    date = boosted_positive_rate_df['date'].tolist()
    vaccinated = boosted_positive_rate_df['new_vaccinations_smoothed_per_million'].tolist()

    return render_template('boosted_positive_rate.html', labels=date, positive=positive, boosted=boosted,
                           vaccinated=vaccinated)


@app.route("/population_vaccinated")
def population_vaccinated():
    population_vaccinated_df = query_data.get_population_vaccinated()

    population = population_vaccinated_df['population'].tolist()
    vaccinated = population_vaccinated_df['total_vaccinations_per_hundred'].tolist()
    countries = population_vaccinated_df['location'].tolist()

    return render_template('population_vaccinated.html', population=population, vaccinated=vaccinated,
                           labels=countries)


@app.route("/lockdown_deaths")
def lockdown_deaths():
    lockdown_deaths_df = query_data.get_stringency_death_rate()

    deaths = lockdown_deaths_df['total_deaths_per_million'].tolist()
    stringency = lockdown_deaths_df['stringency_index'].tolist()
    countries = lockdown_deaths_df['location'].tolist()
    cases = lockdown_deaths_df['total_cases_per_million'].tolist()
    scaled_cases = [i/10000 for i in cases]

    return render_template('lockdown_deaths.html', deaths=deaths, stringency=stringency, labels=countries,
                           cases=scaled_cases)


if __name__ == "__main__":
    app.run(debug=True)
