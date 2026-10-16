import pandas as pd
from pathlib import Path

data_folder = Path("sample_data")

csv_files = list(data_folder.glob("*.csv"))

print("찾은 CSV 파일:")
for file in csv_files:
    print(file)

dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

combined = pd.concat(dataframes, ignore_index=True)

cleaned = combined.drop_duplicates()

cleaned.to_excel("cleaned_sales.xlsx", index=False)

print()
print("완료!")
print(f"처리한 파일 수: {len(csv_files)}")
print(f"원본 행 수: {len(combined)}")
print(f"중복 제거 후 행 수: {len(cleaned)}")