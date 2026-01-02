import pandas as pd
from pathlib import Path



def read_excel_report(path: Path) -> pd.DataFrame:

    return pd.read_excel(path,"Monthly Summary",skiprows=1, header=[0,1])

