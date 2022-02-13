from flask import Flask, render_template
from covidVisualizationTool.queries.queryData import QueryData as qd

app = Flask(__name__)


@app.route("/", methods=("POST", "GET"))
def home():
    query_data = qd(db_location="/Users/lizjeukeng/PycharmProjects/UmassD/gradproject/docs/test_db.db"). \
        get_death_rate_partially_vaccinated()

    return render_template('index.html', data=query_data)


@app.route("/vaccinated_deaths")
def vaccinated_deaths():
    return render_template('vaccinated_deaths.html')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
