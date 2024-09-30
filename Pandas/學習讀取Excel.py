import pandas as pd
import os

# Got excel directory
dirictory = os.path.dirname(__file__)
# Got excel name
Excel_name = "Target_Data.xlsx"
# Got excel path
Path_file = dirictory + "/" + Excel_name

# Then open the Excel and open the sheet1
data_Frame = pd.read_excel(Path_file, sheet_name="工作表1")
print("Data frame\n", data_Frame)
print("Get the type \n", type(data_Frame))

# Then try to load header "C_directory1"
data_frame_Header_C_directory1 = data_Frame["C_directory1"]
print("data_frame_Header_C_directory1\n",data_frame_Header_C_directory1)
print("Get the type \n", type(data_frame_Header_C_directory1))

# also if i don't know head in this worksheet we can use this
data_frame_head_info = data_Frame.columns
print("data_frame_head_info\n",data_frame_head_info)
print("Get the type \n", type(data_frame_head_info))
print("data_frame_Header_C_directory1\n", data_Frame.head(2)) # 顯示該data_Frame的列數
print("Get the type \n", type(data_frame_head_info))


# If i want to replace the value in "data_frame_Header_C_directory1"

print(f"in the data frame C column 3 row dirictory value :{data_frame_Header_C_directory1[2]}")
print(f"Get the index :\n{data_Frame.index}")
print(f"Get the value :\n{data_Frame.values}")
