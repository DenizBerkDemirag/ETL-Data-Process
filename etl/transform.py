import pandas as pd

def clean_whitespace(df: pd.DataFrame) -> pd.DataFrame:

    string_columns = df.select_dtypes(include= "object").columns

    for column in string_columns:
        df[column] = df[column].str.strip()
    return df

def replace_invalid_values(df: pd.DataFrame) -> pd.DataFrame:

    invalid_values = ["N/A", "UNKNOWN", "FREE", "", "NULL"]

    df = df.replace(invalid_values, pd.NA)

    return df

