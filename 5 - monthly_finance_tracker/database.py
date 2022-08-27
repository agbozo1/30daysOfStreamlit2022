from deta import Deta
from dotenv import load_dotenv
import os
#https://www.toptal.com/developers/gitignore/

#https://deta.sh/ - database
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

db = deta.Base("finance_tracker")

#store 
def insert_period(period, incomes, expenses,comment):
    return db.put({"key":period, "incomes":incomes, "expenses":expenses, "comment":comment})

#
def fetch_all_periods():
    results = db.fetch()
    return results.items

#get specific period
def get_period(period):
    return db.get(period)