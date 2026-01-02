from load import load
from extract import read_excel_report
from transform import transform 
from pathlib import Path

#get excel file from sibling folder 'data'
BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "data" / "Diagnostic Summary.xlsx"



def run():
    df_raw = read_excel_report(EXCEL_PATH)
    df = transform(df_raw)
    load(df)

if __name__ == "__main__": #guards against running run() on import
    run()
