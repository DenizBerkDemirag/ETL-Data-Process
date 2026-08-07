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


def standardize_order_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["order_id"] = df["order_id"].astype("string").str.strip()

    # #1007 -> ORD-1007
    df["order_id"] = df["order_id"].str.replace(
        r"^#(\d+)$",
        r"ORD-\1",
        regex=True
    )

    # 1011 -> ORD-1011
    df["order_id"] = df["order_id"].str.replace(
        r"^(\d+)$",
        r"ORD-\1",
        regex=True
    )

    return df


def remove_invalid_order_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Geçerli format: ORD- + bir veya daha fazla rakam
    valid = df["order_id"].str.match(
        r"^ORD-\d+$",
        na=False
    )

    return df[valid].copy()


def deduplicate_order_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["_filled_count"] = df.notna().sum(axis=1)

    df = (
        df.sort_values("_filled_count", ascending=False)
          .drop_duplicates("order_id", keep="first")
          .sort_index()
          .drop(columns="_filled_count")
    )

    return df


def normalize_name(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    df["customer_name"] = (df["customer_name"]
                            .str.strip()
                            .str.replace(r"\s+", " ", regex=True)
                            .str.lower()
                            .str.title()
                            )
    
    return df

def split_name(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    df[["first_name", "last_name"]] = (
        df["customer_name"]
        .str.rsplit(" ", n=1, expand=True)
    )

    return df


def standardize_email(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    df["customer_email"] = (
        df["customer_email"]
        .str.lower()
        .str.strip()
    )

    return df

def remove_invalid_emails(df: pd.Dataframe) -> pd.Dataframe:
    df = df.copy()
    
    valid = df["customer_email"].str.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", na=False)
    
    return df[valid].copy()


def standardize_phone_numbers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["phone_number"] = (
        df["phone_number"]
        .astype("string")
        .str.replace(r"\D", "", regex=True)
    )

    df["phone_number"] = df["phone_number"].str.replace(
        r"^90",
        "0",
        regex=True
    )

    df["phone_number"] = df["phone_number"].where(
        df["phone_number"].str.startswith("0"),
        "0" + df["phone_number"]
    )

    return df

def remove_invalid_phone_numbers(df: pd.Dataframe) -> pd.Dataframe:
    df = df.copy()
    
    valid = df["phone_number"].str.match(r"^05\d{9}$", na=False)

    df.loc[~valid, "phone_number"] = pd.NA
    
    return df

def standardize_order_dates(df: pd.Dataframe) -> pd.DataFrame:
    df = df.copy()

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="mixed",
        errors="coerce"
    )

    return df