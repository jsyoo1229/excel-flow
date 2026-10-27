import pandas as pd
from pathlib import Path


# Set the folder containing the CSV files
data_folder = Path("sample_data")

# Find all CSV files in the folder
csv_files = list(data_folder.glob("*.csv"))

# Stop the program if no CSV files are found
if not csv_files:
    print("No CSV files found in the sample_data folder.")
    exit()

# Display the CSV files that were found
print("CSV files found:")
for file in csv_files:
    print(file)


# Read each CSV file and store it together with its file path
dataframes = []

for file in csv_files:
    try:
        df = pd.read_csv(file)

        # Remove leading and trailing whitespace from column names
        df.columns = df.columns.str.strip()
        dataframes.append((file, df))
    except Exception as e:
        # Continue processing even if one file cannot be read
        print(f"Failed to read file: {file}")
        print(f"Error: {e}")

# Stop the program if none of the CSV files could be read
if not dataframes:
    print("No CSV files could be read.")
    exit()


# Count how often each column structure appears
column_counts = {}

for file, df in dataframes:
    # Convert column names to a tuple so they can be used as a dictionary key
    columns = tuple(df.columns)

    if columns in column_counts:
        column_counts[columns] += 1
    else:
        column_counts[columns] = 1

# Use the most common column structure as the expected structure
main_columns = max(column_counts, key=column_counts.get)


# Keep only CSV files that match the most common column structure
valid_dataframes = []

for file, df in dataframes:
    if tuple(df.columns) == main_columns:
        valid_dataframes.append(df)
    else:
        print(f"Skipped: {file} (column structure does not match)")


# Combine all valid CSV files into one DataFrame
combined = pd.concat(valid_dataframes, ignore_index=True)




# Clean text columns
for column in combined.select_dtypes(include="str").columns:
    # Remove leading and trailing whitespace from text values
    combined[column] = combined[column].str.strip()

    # Convert empty strings to missing values
    combined[column] = combined[column].replace("", pd.NA)


# Find text-like columns that may contain numeric values
string_columns = combined.select_dtypes(include="str").columns.tolist()

# Include object columns separately for compatibility with newer pandas versions
object_columns = combined.select_dtypes(
    include="object",
    exclude="str"
).columns.tolist()

candidate_columns = string_columns + object_columns


# Try to convert numeric-looking text columns into actual numeric columns
for column in candidate_columns:
    cleaned_values = (
        combined[column]
        .astype("string")
        # Remove thousands separators
        .str.replace(",", "", regex=False)
        # Remove dollar signs
        .str.replace("$", "", regex=False)
    )

    # Convert values to numbers.
    # Values that cannot be converted become missing values.
    numeric_values = pd.to_numeric(
        cleaned_values,
        errors="coerce"
    )

    # Check only the values that were not originally missing
    non_missing = combined[column].notna()

    # Convert the column only if all existing values
    # were successfully converted
    if numeric_values[non_missing].notna().all():
        combined[column] = numeric_values


# Try to detect and convert date columns
for column in combined.select_dtypes(include="str").columns:
    try:
        # Try to parse text values as dates
        parsed_dates = pd.to_datetime(
            combined[column],
            format="mixed",
            errors="coerce"
        )

        # Check only the values that were not originally missing
        non_missing = combined[column].notna()

        # Convert the column only if all existing values
        # were successfully parsed as dates
        if parsed_dates[non_missing].notna().all():
            combined[column] = parsed_dates

    except Exception:
        # Leave the column unchanged if date parsing fails
        pass


# Display column data types after automatic conversions
print()
print("Detected column types:")
print(combined.dtypes)


# Remove duplicate rows
cleaned = combined.drop_duplicates()

# Remove rows containing missing values
cleaned = cleaned.dropna()


# Export the cleaned data to an Excel file
cleaned.to_excel("cleaned_sales.xlsx", index=False)


# Display a summary of the cleaning process
print()
print("Done!")
print(f"Files processed: {len(valid_dataframes)}")
print(f"Files skipped: {len(dataframes) - len(valid_dataframes)}")
print(f"Original rows: {len(combined)}")
print(f"Cleaned rows: {len(cleaned)}")