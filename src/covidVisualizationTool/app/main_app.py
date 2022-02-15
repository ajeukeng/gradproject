from flask import Flask, render_template
from covidVisualizationTool.queries.queryData import QueryData as qd
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/", methods=("POST", "GET"))
def home():
    return render_template('index.html')


@app.route("/vaccinated_deaths")
def vaccinated_deaths():
    query_data = qd(db_location="/Users/lizjeukeng/PycharmProjects/UmassD/gradproject/docs/cvt-test.db"). \
        get_death_rate_partially_vaccinated()

    df = pd.read_sql(query_data.statement,
                     con=qd(
                         db_location="/Users/lizjeukeng/PycharmProjects/UmassD/gradproject/docs/cvt-test.db").session.bind)
    df['new_deaths_smoothed_per_million'] = df['new_deaths_smoothed_per_million'].fillna(0)
    df['new_vaccinations_smoothed_per_million'] = df['new_vaccinations_smoothed_per_million'].fillna(0)
    vaccinated = df['new_vaccinations_smoothed_per_million'].tolist()
    labels = df["date"].tolist()
    values = df["new_deaths_smoothed_per_million"].tolist()
    print(labels)
    print(values)

    return render_template('vaccinated_deaths.html', max=20000, values=values[351:], labels=labels[351:],
                           vaccinated=vaccinated[351:])


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/positive_rate_by_population_density")
def positive_rate_by_population_density():
    return render_template('positive_rate_by_population_density.html')


@app.route("/median_age_death_rate")
def median_age_death_rate():
    return render_template('median_age_death_rate.html')


@app.route("/positive_rate_for_total_tests")
def positive_rate_for_total_tests():
    return render_template('positive_rate_for_total_tests.html')


@app.route("/icu_patients_vaccinations")
def icu_patients_vaccinations():
    return render_template('icu_patients_vaccinations.html')


@app.route("/boosted_positive_rate")
def boosted_positive_rate():
    return render_template('boosted_positive_rate.html')


@app.route("/population_vaccinated")
def population_vaccinated():
    return render_template('population_vaccinated.html')


if __name__ == "__main__":
    app.run(debug=True)
