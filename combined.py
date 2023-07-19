import pandas as pd
df_a = pd.read_excel('companies.xlsx')  # Replace 'file_a.xlsx' with the actual filename of File A
df_b = pd.read_excel('companies2.xlsx')  # Replace 'file_b.xlsx' with the actual filename of File B
df_combined = pd.concat([df_a, df_b], ignore_index=True)
df_combined.to_excel('combined_companies.xlsx', index=False)  # Replace 'combined_file.xlsx' with your desired filename
