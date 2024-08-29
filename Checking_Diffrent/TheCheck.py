import pandas as pd
import os
import sys
from difflib import get_close_matches

def find_newest_and_oldest_excel_files(directory):
    excel_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.xlsx', '.xlsm', 'csv'))]
    sorted_files = sorted(excel_files, key=lambda x: os.path.getmtime(x))
    return (sorted_files[0], sorted_files[-1]) if sorted_files else (None, None)

def read_file(file, sheet_name=None):
    if file.endswith(('.xlsx', '.xlsm')):
        df = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    elif file.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        raise ValueError("不支持的檔案格式")
    print(f"已成功讀取檔案 {file}，以下是檔案的前幾行數據：\n", df.head())
    return df

def find_closest_column(df, column_name):
    match = get_close_matches(column_name, df.columns, n=1, cutoff=0.6)
    return match[0] if match else None

def delete_old_reports(directory):
    old_report_files = ['Txt_to_checking_old_Data.csv', 'Txt_to_checking_new_Data.csv', 'detailed_diff_report.csv']
    for file_name in old_report_files:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"已刪除舊報告文件：{file_name}")
        else:
            print(f"未找到舊報告文件：{file_name}，無需刪除。")

def generate_detailed_diff_report(directory, old_file, new_file, sheet_name, key_columns):
    print("正在比較檔案：", old_file, new_file)
    df_old = read_file(old_file, sheet_name=sheet_name)
    print("舊檔案的列名：", df_old.columns.tolist())
    print(f"已完成讀取舊檔案：{old_file}")
    
    df_new = read_file(new_file, sheet_name=sheet_name)
    print("新檔案的列名：", df_new.columns.tolist())
    print(f"已完成讀取新檔案：{new_file}")
    
    # 檢查並匹配列名
    key_columns = [find_closest_column(df_old, col) for col in key_columns]
    print("匹配後的關鍵列名：", key_columns)
    
    if None in key_columns:
        print("錯誤：無法在數據中找到與 key_columns 匹配的列名。")
        return
    
    print("正在生成舊檔案和新檔案的 CSV 文件以便檢查...")
    df_old.to_csv(os.path.join(directory, 'Txt_to_checking_old_Data.csv'), index=True, sep='\t', encoding='utf-8-sig')
    df_new.to_csv(os.path.join(directory, 'Txt_to_checking_new_Data.csv'), index=True, sep='\t', encoding='utf-8-sig')
    print("已生成 CSV 文件")

    print("正在依據唯一標識符合併數據...")
    df_old['Unique Identifier'] = df_old.index.astype(str) + '_' + df_old[key_columns].astype(str).agg('_'.join, axis=1)
    print("舊檔案的唯一標識符生成完成")
    df_new['Unique Identifier'] = df_new.index.astype(str) + '_' + df_new[key_columns].astype(str).agg('_'.join, axis=1)
    print("新檔案的唯一標識符生成完成")
    
    print("正在設置唯一標識符為索引...")
    df_old.set_index('Unique Identifier', inplace=True)
    print("舊檔案的唯一標識符已設置完成")
    df_new.set_index('Unique Identifier', inplace=True)
    print("新檔案的唯一標識符已設置完成")
    
    print("正在查找新增的列...")
    new_columns = df_new.columns.difference(df_old.columns)
    print("找到的新增列：", new_columns)
    
    print("正在查找新增和刪除的行...")
    added_rows = df_new[~df_new.index.isin(df_old.index)]
    print("找到的新增行：", added_rows)
    removed_rows = df_old[~df_old.index.isin(df_new.index)]
    print("找到的刪除行：", removed_rows)
    
    common_index = df_old.index.intersection(df_new.index)
    df_old_common = df_old.loc[common_index]
    df_new_common = df_new.loc[common_index]
    
    df_old_common, df_new_common = df_old_common.align(df_new_common, join='inner', axis=1)

    df_old_common = df_old_common.sort_index()
    df_new_common = df_new_common.sort_index()

    diff_mask = (df_old_common != df_new_common) & ~(df_old_common.isnull() & df_new_common.isnull())
    differences = diff_mask.any(axis=1)

    csv_path = os.path.join(directory, "detailed_diff_report.csv")
    report_data = []

    if not differences.any() and added_rows.empty and removed_rows.empty and new_columns.empty:
        report_data.append(['檔案之間沒有發現任何差異。'])
    else:
        if not new_columns.empty:
            report_data.append(['發現新增的欄位：'])
            for col in new_columns:
                report_data.append([f"在新檔案 '{os.path.basename(new_file)}' 中，發現欄位 '{col}' 存在，但在舊檔案 '{os.path.basename(old_file)}' 中不存在此欄位。"])
            report_data.append([])

        if not added_rows.empty:
            report_data.append([f"在新檔案 '{os.path.basename(new_file)}' 中，發現新增的行："])
            added_rows_data = added_rows.reset_index().values.tolist()
            for row in added_rows_data:
                report_data.append([f"行資料：{row}"])
            report_data.append([])

        if not removed_rows.empty:
            report_data.append([f"在舊檔案 '{os.path.basename(old_file)}' 中，發現已刪除的行："])
            removed_rows_data = removed_rows.reset_index().values.tolist()
            for row in removed_rows_data:
                report_data.append([f"行資料：{row}"])
            report_data.append([])

        for i in differences[differences].index:
            report_data.append([f"在索引 {i} 發現資料變動："])
            old_values = df_old_common.loc[i, diff_mask.loc[i]]
            new_values = df_new_common.loc[i, diff_mask.loc[i]]
            for col in old_values.index:
                report_data.append([
                    f"在欄位 '{col}' 發現變更：在舊檔案 '{os.path.basename(old_file)}' 中的值為 '{old_values[col]}'，"
                    f"而在新檔案 '{os.path.basename(new_file)}' 中的值為 '{new_values[col]}'。"
                ])
            report_data.append([])  # 添加一個空行以區分每個索引的差異

    print("正在將差異報告寫入 CSV 文件...")
    pd.DataFrame(report_data).to_csv(csv_path, index=False, header=False, encoding="utf-8-sig")
    print(f"差異報告已成功保存至 {csv_path}")

def main():
    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.abspath(__file__))
    print("當前目錄：", directory)

    # 在尋找最新和最舊檔案之前，刪除舊的報告文件
    delete_old_reports(directory)
    
    old_file, new_file = find_newest_and_oldest_excel_files(directory)
    if not old_file or not new_file:
        print("未找到 Excel 或 CSV 檔案。")
        return
    print("最新的檔案：", new_file)
    print("最舊的檔案：", old_file)

    sheet_name = "sheet1"  
    key_columns = ["管線材質", "ORDER_SEQ", "品名", "重組"]
    print("工作表名稱：", sheet_name)
    print("唯一標識符列：", key_columns)
    print("正在生成詳細差異報告...")
    generate_detailed_diff_report(directory, old_file, new_file, sheet_name, key_columns)
    print("詳細差異報告生成完成。")

if __name__ == "__main__":
    main()
