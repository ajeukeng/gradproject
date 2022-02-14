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
    query_data = qd(db_location="/Users/lizjeukeng/PycharmProjects/UmassD/gradproject/docs/test_db.db"). \
        get_death_rate_partially_vaccinated()

    df = pd.read_sql(query_data.statement,
                     con=qd(
                         db_location="/Users/lizjeukeng/PycharmProjects/UmassD/gradproject/docs/test_db.db").session.bind)
    df['new_deaths'] = df['new_deaths'].fillna(0)
    df['people_vaccinated'] = df['people_vaccinated'].fillna(0)
    labels = df["date"].tolist()
    values = df["new_deaths"].tolist()
    print(labels)
    print(values)

    return render_template('vaccinated_deaths.html', max= 10000, values=values, labels=labels)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
