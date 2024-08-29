import pandas as pd

# 使用原始字串來定義路徑，避免反斜線需要雙寫
directoryforfile = r'G:\我的雲端硬碟\Python_Tool-main\領用料總表\\'

# 讀取 Excel 資料，並將所有資料轉換為字串類型
df = pd.read_excel(directoryforfile + '113.08.24_領用料總表.xlsx', sheet_name='tocl', dtype=str)

# 初始化一个日志记录列表
log_data = []

def log(message):
    """将日志信息添加到 log_data 列表中。"""
    log_data.append(message)
    print(message)  # 可选：如果你仍希望在控制台输出

# 顯示資料
log("領料表:")
log(df.head().to_string())  # 只顯示前幾行以避免打印過多數據

# 將原始資料儲存為 txt 檔案以便檢查
df.to_csv(directoryforfile + 'Txt_to_checking.txt', index=False, sep='\t', encoding='utf-8-sig')

# 保留 A 列到合計2 列的所有資料
preserved_df = df.loc[:, :"合計2"]
log("保留的資料區段:")
log(preserved_df.head().to_string())

# 初始化最終的 DataFrame
final_df = pd.DataFrame()

# 定義一個函數來填充列表到指定長度
def fill_to_length(lst, length):
    return lst + [''] * (length - len(lst))

# 初始化日期報告的數據結構
csv_to_storage_report = []

# 自動識別日期列（假設日期列名稱是像 "7/2", "7/9" 這樣的格式）
date_columns = [col for col in df.columns if "/" in col]
log(f"識別到的日期列: {date_columns}")

# 根據日期列自動識別對應的項目區域
item_headers = ["-", "A", "B", "D", "E"]
log(f"項目標頭: {item_headers}")

# 初始化項目與其對應日期列的字典
date_groups = {header: [] for header in item_headers}
log("初始化日期列分組:")

# 根據7/2.*的前綴來切換到下一個項目
group_index = 0
for col in date_columns:
    # 解析日期列名，去掉索引部分 (如 ".1", ".2" 等)
    base_col = col.split('.')[0]

    # 當遇到新的 "7/2" 系列日期時，切換到下一個項目
    if base_col == '7/2' and len(date_groups[item_headers[group_index]]) > 0:
        group_index += 1
        if group_index >= len(item_headers):
            break
        log(f"遇到新的 7/2 開頭列，切換到項目 {item_headers[group_index]}")
    
    date_groups[item_headers[group_index]].append(col)
    log(f"正在分配日期列 {col} 給項目 {item_headers[group_index]}")

# 打印分配結果
for header, columns in date_groups.items():
    log(f"項目 {header} 分配的日期列: {columns}")

# 找到最長的日期列數
max_date_columns = max([len(date_groups[header]) for header in item_headers])
log(f"最長的日期列數: {max_date_columns}")

# 逐行處理每一行資料
for index, row in df.iterrows():
    log(f"\n正在處理第 {index} 行數據...")
    date_data = {}
    
    # 提取每個項目對應的日期數據，並填充至最大列數
    for item in item_headers:
        date_data[item] = fill_to_length([row[col] for col in date_groups[item]], max_date_columns)
        log(f"項目 {item} 的日期數據: {date_data[item]}")

    # 將所有日期相關數據加入報告列表
    csv_to_storage_report.append({
        "項目": f"Row_{index}",
        **{item: date_data[item] for item in item_headers}
    })

    # 提取設計需求、採購需求和缺料狀況列的資料
    設計需求 = row[date_groups['-']]
    採購需求 = row[[f"{item}.1" for item in item_headers]]
    缺料狀況 = row[[f"{item}.2" for item in item_headers]]

    log(f"設計需求: {設計需求.tolist()}")
    log(f"採購需求: {採購需求.tolist()}")
    log(f"缺料狀況: {缺料狀況.tolist()}")

    # 確保所有序列長度一致
    max_length = max(len(設計需求), len(採購需求), len(缺料狀況))
    log(f"當前最大長度: {max_length}")

    # 使用 None 填充不足的部分
    設計需求 = fill_to_length(設計需求.tolist(), max_length)
    採購需求 = fill_to_length(採購需求.tolist(), max_length)
    缺料狀況 = fill_to_length(缺料狀況.tolist(), max_length)

    # 提取並填充 preserved_df 和 "用料時機" 列的值，用來放入新創建的行
    preserved_values = preserved_df.iloc[index].tolist()
    preserved_values.append(row["用料時機"])
    preserved_values += [None] * (len(設計需求) - 2)
    log(f"保留的值: {preserved_values}")

    # 組合重組後的數據
    restructured_df = pd.DataFrame({
        "項目": item_headers,
        "設計需求": 設計需求,
        "採購需求": 採購需求,
        "缺料狀況": 缺料狀況,
        **{f"{col}_{i}": [date_data[item][i] for item in item_headers] for i, col in enumerate(date_columns[:max_date_columns])}
    })

    # 將保留的資料插入新行的前幾列，避免重複插入已存在的列
    for i, col in enumerate(preserved_df.columns):
        if col not in restructured_df.columns:
            restructured_df.insert(i, col, [preserved_values[i]] + [None] * (len(設計需求) - 1))
            log(f"插入保留列 {col} 至 DataFrame")

    # 插入 "用料時機" 列，確保不重複
    if "用料時機" not in restructured_df.columns:
        restructured_df["用料時機"] = [row["用料時機"]] + [None] * (len(設計需求) - 1)
        log("插入用料時機列")

    # 為了避免索引重複，使用原始索引 + 項目名稱作為新索引
    restructured_df.index = [f"{index}_{item}" for item in restructured_df["項目"]]
    log(f"重組後的 DataFrame 索引: {restructured_df.index}")

    # 合併保留的資料與重組後的資料
    combined_df = pd.concat([restructured_df.reset_index(drop=True)], axis=1)
    log(f"合併後的 DataFrame:\n{combined_df.head()}")

    # 將每一行的結果合併到最終的 DataFrame 中
    final_df = pd.concat([final_df, combined_df], ignore_index=True)

# 生成 csv_to_storage_report 的 DataFrame
storage_report_df = pd.DataFrame.from_records(csv_to_storage_report)

# 展開每個列中的列表以生成多列格式
expanded_storage_report_df = storage_report_df.explode(list(storage_report_df.columns[1:]))
log(f"生成的存儲報告 DataFrame:\n{expanded_storage_report_df.head()}")

# 保存日期相關報告到 CSV 檔案
expanded_storage_report_df.to_csv(directoryforfile + 'csv_to_storage_report.csv', index=False, encoding='utf-8-sig')
log(f"日期報告已保存至: {directoryforfile + 'csv_to_storage_report.csv'}")

# 顯示最終的 DataFrame
log("最終的重組 DataFrame:")
log(final_df.head().to_string())

# 保存結果到 CSV 檔案
final_df.to_csv(directoryforfile + r'重組後的領料表.csv', index=False, encoding='utf-8-sig')
log(f"CSV 檔案已保存至: {directoryforfile + r'重組後的領料表.csv'}")

# 保存日志信息到 CSV 文件
log_df = pd.DataFrame(log_data, columns=["Log"])
log_file = directoryforfile + 'processing_log.csv'
log_df.to_csv(log_file, index=False, encoding='utf-8-sig')
log(f"所有日志信息已保存至: {log_file}")
