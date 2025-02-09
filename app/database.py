from sqlalchemy import create_engine
import pandas as pd

DB_URL = "sqlite:///his_database.db"
engine = create_engine(DB_URL)

def create_tables():
    sheets = ["Physicians", "Schedules", "Specialities", "Pricelist", "Policy"]
    xls = pd.ExcelFile("data/HIS_data.xlsx")

    for sheet in sheets:
        df = xls.parse(sheet)
        df.to_sql(sheet, engine, if_exists="replace", index=False)

if __name__ == "__main__":
    create_tables()
