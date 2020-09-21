
import sys
import os

from commonutils.CompanyScraper import CompanyScraper
import pandas as pd
import csv


company_data = []


# csv file name
filename = "Book1.csv"

with CompanyScraper() as scraper:
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            print(row)
            overview = scraper.scrape(company=row)
            overview['company_name'] = row[1]
            overview['company_link'] = row[0]
            company_data.append(overview)
            df = pd.DataFrame(company_data)
            df.to_csv('out.csv', index=False)
            break

