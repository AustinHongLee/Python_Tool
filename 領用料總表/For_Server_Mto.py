
import pandas as pd

# dimentional data and the path of the file and the sheet name and the output file
path = r'C:\Users\a0976\Desktop\領用料總表\重組後的領料表.xlsx'
sheet_name = '重組後的領料表'
output_file = r'C:\Users\a0976\Desktop\領用料總表\重組後的領料表_fill_missing_Value.csv'

# Read the data from the excel file and get the headers

excel = pd.ExcelFile(path)
df = excel.parse(sheet_name)
headers = df.columns.tolist()

print("原始資料:")
print(df)



# Action 1 : Create a Head Range list to store the range of each header and ffill the missing values
head_range = ['管線材質', 'ORDER_SEQ', 'Short_desc', 'SIZE1', 'SIZE2', 'SCH1', 'SCH2', 'SIZE_LAYOUT', '厚度', 'UNIT', 'IDENT_CODE' ,'用料時機', '中文說明']

for head in head_range:
    df[head] = df[head].ffill()
# Action 2 : join the ident_code and the item to create a new column called "重組"
df['重組'] = df['IDENT_CODE'] + '_' + df['項目']    

# Output the result to output_file
df.to_csv(output_file, index=False, encoding='utf-8-sig')    

print("\n Done! Please check the output file: ", output_file)