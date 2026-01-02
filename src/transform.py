import pandas as pd


def flatten_window(df: pd.DataFrame, metric: str):

    df = df.copy()

    if not isinstance(df.columns, pd.MultiIndex): #guard against unexpected source/processing format. Should be a multilevel index
        raise TypeError("Expected MultiIndex columns from Excel input")

    #rename the first 2 columns. Create new object where the first 2 are named and the remaining ones are defaulted to the original column names
    #As the columns are a multiindex (due to the date stacking with provider), columns are in tuples - 'meta' is a placeholder name
    df.columns = pd.MultiIndex.from_tuples(
        [
            ("meta", "Type"),
            ("meta", "Modality"),
            *df.columns[2:] 
        ]
    )

    df = (
        df
        .melt(
            id_vars=[("meta", "Type"), ("meta", "Modality")], #we want to unpivot all other columns, so keep the type/modality
            var_name=["Date", "Source"], #unpivoting multi index so provide both values here
            value_name="Value" #value in matrix being unpivoted
        )
    )
    df.columns = [
        "Type",
        "Modality",
        *df.columns[2:]
    ] 

    df["Type"] = df["Type"].ffill() #Type is merged in spreadsheet so needs filling down

    df = df[ df["Source"].isin(['Source A','Source B'])].copy() #.copy used here to avoid the risk of updating a view - the isin filter could potentially return a view

    df["Metric"] = metric

    return df




def transform(df: pd.DataFrame) -> pd.DataFrame:
#Reshape Excel matrix data into a normalized reporting format
        
    #find rows where data starts and ends in the source data
    #index property returns a list of values, so get the first (should only be one anyway)
    df_total_end = df[df[("Unnamed: 1_level_0","WAITING LIST")] == 'Total waiters'].index[0]-1 #cutoff for first matrix. index returns a list of values, so get the first (should only be one anyway)
    df_total_window = flatten_window(df.loc[:df_total_end],"Waiting List") #define first window of data

    df_6w_breach_start = df[df[("Unnamed: 1_level_0","WAITING LIST")] == '6+ WEEK BREACHES'].index[0]+1 #get start of second matrix
    df_6w_breach_end = df[df[("Unnamed: 1_level_0","WAITING LIST")] == 'Total 6+ Week Breaches'].index[0]-1 #get end of second matrix
    df_6w_breach_window = flatten_window(df.loc[df_6w_breach_start:df_6w_breach_end], "6+ Week Breaches") #define 6 week waiter window

    df_combined = pd.concat([df_6w_breach_window,df_total_window]) #combine windows

    df_combined : pd.DataFrame = df_combined[df_combined["Value"].notna()] #remove nulls

    df_combined["Value"] = pd.to_numeric(df_combined["Value"], errors="coerce").astype(int)

    return df_combined[["Metric", "Date", "Value", "Source", "Modality", "Type"]]
