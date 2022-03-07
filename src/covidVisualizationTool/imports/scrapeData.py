import os

import requests
import csv
from datetime import date
from common_utilities import CommonUtilities as cu


class ScrapeData:
    def __init__(self):
        self.data_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
        self.csv_filename = os.path.join('docs', f'cvt_raw_csv_{date.today()}.csv')
        self.cvt_logger = cu().cvt_logger()

    def get_covid_data(self):
        with requests.Session() as s:
            download = s.get(self.data_url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            data_list = list(cr)
            with open(self.csv_filename, 'w') as f:
                writer = csv.writer(f)
                for row in data_list:
                    writer.writerow(row)
                    self.cvt_logger.info(row)
