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
        dataframes.append((file, df))
    except Exception as e:
        print(f"Failed to read file: {file}")
        print(f"Error: {e}")
        
if not dataframes:
    print("No CSV files could be read.")
    exit()        
    
column_counts = {}

for file, df in dataframes:
    columns = tuple(df.columns)
    
    if columns in column_counts:
        column_counts[columns] += 1
    else:
        column_counts[columns] = 1 
        
main_columns = max(column_counts, key=column_counts.get)        

valid_dataframes = []

for file, df in dataframes:
    if tuple(df.columns) == main_columns:
        valid_dataframes.append(df)
    else:
        print(f"Skipped: {file} (column structure does not match)")

combined = pd.concat(valid_dataframes, ignore_index=True)
combined.columns = combined.columns.str.strip()

for column in combined.select_dtypes(include="str").columns:
    combined[column] = combined[column].str.strip()
    combined[column] = combined[column].replace("", pd.NA)

cleaned = combined.drop_duplicates()
cleaned = cleaned.dropna()


cleaned.to_excel("cleaned_sales.xlsx", index=False)

print()
print("Done!")
print(f"Files processed: {len(valid_dataframes)}")
print(f"Files skipped: {len(dataframes) - len(valid_dataframes)}")
print(f"Original rows: {len(combined)}")
print(f"Cleaned rows: {len(cleaned)}")