# Covid Visualization Tool

## About

- The purpose of this application is to display specific correlations from a Covid-19 datasets. 
- The dataset used for this application can be found here: https://github.com/owid/covid-19-data

## Correlations
- Did the death rate from COVID-19 decrease when more people were vaccinated? 
- Does a high population density mean more COVID-19 infections? 
- Does a higher median age mean more COVID-19 deaths?
- Is the positivity rate higher when there are a higher number of new COVID-19 tests? 
- Does the number of ICU patients decrease when the vaccinations increase? 
- Does the number of people boosted affect the positivity test rate? 
- Does a smaller population mean more people get vaccinated? 
- Do stricter lockdown policies mean fewer deaths?

## Create cvt development environment

To establish your development environment, clone this repo and install it as an editable package via pip:

```bash
cd /where/you/want/the/source_code
git clone http://REPOSITORY_NAME_URL
cd REPOSITORY_NAME
pip install --user --editable .
```

If a virtual environment is being used:

```bash
cd /where/you/want/the/source_code
git clone http://REPOSITORY_NAME_URL
cd REPOSITORY_NAME
python3 -m venv venv
. venv/bin/activate
pip install --user --editable .
```

## Usage
- Use `cvt` to run the cli application
  - import-data: Imports data from csv file into database
    - `cvt import-data CSV_FILENAME DATEBASE`
  - query-data: Completes SQL queries on database
    - `cvt query-data DATABASE`
  - get-data: Retrieves raw csv data directly from github repo
    - `cvt get-data`
  - automated-import: Retrieves raw data from site and imports data from csv file to database
    - `cvt automated-import`

- To run the web application
  - `python src/covidVisualizationTool/app/main_app.py`

#### Updating requirements.txt

```bash
# assumes you are at the repository's root directory
# If required, activate the virtual environment
# . venv/bin/activate
pip freeze > requirements.txt
```

#### Viewing Site
- The Covid Visualization Tool production version is located at this url: https://covid-visualization-tool.herokuapp.com/ .