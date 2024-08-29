import pandas as pd

# 定义文件路径
directoryforfile = r'C:\Users\a0976\Desktop\領用料總表\\'
input_file = directoryforfile + '113.08.24_領用料總表.xlsx'

# 读取 Excel 文件
df = pd.read_excel(input_file, sheet_name='tocl', dtype=str)

# 定义一个函数来记录并打印日志
log_data = []

def log(message):
    """将日志信息添加到 log_data 列表中。"""
    log_data.append(message)
    print(message)

# 提取日期列（以 '/' 作为标识）
date_columns = [col for col in df.columns if "/" in col]
log(f"识别到的日期列: {date_columns}")

# 项目标头
item_headers = ["-", "A", "B", "D", "E"]
log(f"项目标头: {item_headers}")

# 初始化一个字典来保存每个项目的日期列
date_groups = {header: [] for header in item_headers}
log("初始化日期列分组:")

# 按顺序分配日期列给对应的项目
group_index = 0
for col in date_columns:
    base_col = col.split('.')[0]  # 处理类似 "7/2.1" 的列名，获取基础日期
    if base_col == '7/2' and len(date_groups[item_headers[group_index]]) > 0:
        group_index += 1
        if group_index >= len(item_headers):
            break
        log(f"遇到新的 7/2 开头列，切换到项目 {item_headers[group_index]}")
    
    date_groups[item_headers[group_index]].append(col)
    log(f"正在分配日期列 {col} 给项目 {item_headers[group_index]}")

# 打印分配结果
for header, columns in date_groups.items():
    log(f"项目 {header} 分配的日期列: {columns}")

# 开始重新组织数据
final_df = pd.DataFrame()

for index, row in df.iterrows():
    log(f"\n正在处理第 {index} 行数据...")
    
    combined_row = pd.Series(dtype='object')

    for item in item_headers:
        for col in date_groups[item]:
            combined_row[col] = row[col]
            log(f"在列 {col} 中添加值 {row[col]} 对应项目 {item}")

    # 将该行添加到最终的 DataFrame 中
    final_df = final_df.append(combined_row, ignore_index=True)

# 保存结果到 CSV 文件
output_file = directoryforfile + r'重组后的领料表.csv'
final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
log(f"CSV 文件已保存至: {output_file}")

# 保存日志信息到 CSV 文件
log_df = pd.DataFrame(log_data, columns=["Log"])
log_file = directoryforfile + 'processing_log.csv'
log_df.to_csv(log_file, index=False, encoding='utf-8-sig')
log(f"所有日志信息已保存至: {log_file}")
