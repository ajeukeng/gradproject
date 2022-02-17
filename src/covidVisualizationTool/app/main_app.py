from flask import Flask, render_template
from covidVisualizationTool.queries.queryData import QueryData as qd

app = Flask(__name__)
query_data = qd(db_location="/Users/lizjeukeng/PycharmProjects/UmassD/gradproject/docs/cvt-updated.db")


@app.route("/", methods=("POST", "GET"))
def home():
    return render_template('index.html')


@app.route("/vaccinated_deaths")
def vaccinated_deaths():
    death_rate_fully_vaccinated_df = query_data.get_death_rate_fully_vaccinated()

    vaccinated = death_rate_fully_vaccinated_df['new_vaccinations_smoothed_per_million'].tolist()
    labels = death_rate_fully_vaccinated_df["date"].tolist()
    deaths = death_rate_fully_vaccinated_df["new_deaths_smoothed"].tolist()
    print(labels)
    print(deaths)

    return render_template('vaccinated_deaths.html', deaths=deaths, labels=labels,
                           vaccinated=vaccinated)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/positive_rate_by_population_density")
def positive_rate_by_population_density():
    positive_rate_by_population_density_df = query_data.get_positive_rate_by_population_density()
    countries = positive_rate_by_population_density_df['location'].tolist()
    population_density = positive_rate_by_population_density_df['population_density'].tolist()
    positive_rate = positive_rate_by_population_density_df['average_positive_rate'].tolist()

    return render_template('positive_rate_by_population_density.html',
                           results=positive_rate_by_population_density_df, labels=countries,
                           population_density=population_density, positive_rate=positive_rate)


@app.route("/median_age_death_rate")
def median_age_death_rate():
    median_age_death_rate_df = query_data.get_median_age_death_rate()

    return render_template('median_age_death_rate.html', results=median_age_death_rate_df)


@app.route("/positive_rate_for_total_tests")
def positive_rate_for_total_tests():
    positive_rate_for_total_tests_df = query_data.get_positive_rate_for_total_tests()

    return render_template('positive_rate_for_total_tests.html', results=positive_rate_for_total_tests_df)


@app.route("/icu_patients_vaccinations")
def icu_patients_vaccinations():
    icu_patients_vaccinations_df = query_data.get_icu_patients_vaccinations()

    return render_template('icu_patients_vaccinations.html', results=icu_patients_vaccinations_df)


@app.route("/boosted_positive_rate")
def boosted_positive_rate():
    boosted_positive_rate_df = query_data.get_boosted_positive_rate()

    return render_template('boosted_positive_rate.html', results=boosted_positive_rate_df)


@app.route("/population_vaccinated")
def population_vaccinated():
    population_vaccinated_df = query_data.get_population_vaccinated()

    return render_template('population_vaccinated.html', results=population_vaccinated_df)


if __name__ == "__main__":
    app.run(debug=True)
