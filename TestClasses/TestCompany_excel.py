
import sys
import os


sys.path.insert(0, "../commonutils")
import commonutils.utils as utils
import commonutils.common as common
from commonutils.CompanyScraper import CompanyScraper
import pandas as pd


company_data = []

data = pd.read_excel (common.input_file_name)
df = pd.DataFrame(data)
df = df.fillna("NA")
#print (df)
df_new = pd.DataFrame()
with CompanyScraper() as scraper:
    for index, row in df.iterrows():
        print(row)
        #if row[utils.type].notnull and row[utils.headquarters].notnull and row[utils.company_size].notnull and row[utils.people_on_linkedin].notnull:
        if row[utils.linkedin_url] == "NA" :
            df_new = df_new.append(row, ignore_index=True)
            print("ignored as linkedin url is not present ")
        elif row[utils.type] == "NA" and row[utils.headquarters] == "NA"  and row[utils.industry] == "NA" :
            #print(row)
            overview = scraper.scrape(company=row[utils.linkedin_url])
            overview[utils.company_name] = row[utils.company_name]
            overview[utils.linkedin_url] = row[utils.linkedin_url]
            print(overview)
            company_data.append(overview)
            df = pd.DataFrame(company_data)
            df.to_csv('temp.csv', index=False)
            df_new = df_new.append(overview, ignore_index=True)
        else :
            df_new = df_new.append(row, ignore_index=True)
            print("ignored processing as data is already preset in excel")

with pd.ExcelWriter(common.out_file_name) as writer:
    df_new.to_excel(writer, sheet_name='sheet1')
    writer.save()
    writer.close()
