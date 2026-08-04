from etl.extract import read_data, RAW_FILE
from etl.transform import transform_data


df = read_data(RAW_FILE)

df = transform_data(df)

print(df.head())