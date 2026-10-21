import pandas as pd
from pathlib import Path

data_folder = Path("sample_data")

csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    print("No CSV files found in the sample_data folder.")
    exit()

print("CSV files found:")
for file in csv_files:
    print(file)

dataframes = []

for file in csv_files:
    try:
        df = pd.read_csv(file)
        dataframes.append(df)
    except Exception as e:
        print(f"Failed to read file: {file}")
        print(f"Error: {e}")
        
if not dataframes:
    print("No CSV files could be read.")
    exit()        
    
columns = dataframes[0].columns

for df in dataframes[1:]:
    if not df.columns.equals(columns):
        print("Warning: CSV files have different column structures.")

combined = pd.concat(dataframes, ignore_index=True)
combined.columns = combined.columns.str.strip()

for column in combined.select_dtypes(include="str").columns:
    combined[column] = combined[column].str.strip()
    combined[column] = combined[column].replace("", pd.NA)

cleaned = combined.drop_duplicates()
cleaned = cleaned.dropna()


cleaned.to_excel("cleaned_sales.xlsx", index=False)

print()
print("Done!")
print(f"Files processed: {len(csv_files)}")
print(f"Original rows: {len(combined)}")
print(f"Cleaned rows: {len(cleaned)}")