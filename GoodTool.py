import sys
import datetime
import inspect

# 模組使用說明:
# 1. 如果要使用此模組中的函數，您需要先將此模組的路徑加入系統的模組搜尋路徑。請在您的程式碼中加入以下兩行:
#    import sys
#    sys.path.append("模組所在的路徑")  # 例如: sys.path.append(r"G:\我的雲端硬碟\Python_Tool-main")
#    此模組放置於 Python_Tool-main 資料夾 (您可以根據實際情況自行修改路徑)
# 2. 引入模組後，就可以使用其中的函數:
#    from GoodTool import print_step_calculator, reset_print_step, write_file, close_file, toggle_debug_mode
# 3. 各函數功能介紹:
#    - print_step_calculator(words): 打印詳細步驟資訊，包括函數名稱、計數步驟和當前時間
#       - words: 顯示的文字內容 (可選，預設為空白) 建議配合 f-string 使用，方便動態顯示資訊
#    - print_step_calculator_simple(): 打印簡單步驟資訊，僅顯示當前步驟和計數
#    - toggle_debug_mode(state=True): 切換調試模式 (預設開啟調試模式)
#       - state: 若設為 True，則啟用調試模式，設為 False 則關閉
#    - reset_print_step(): 重置計數器 (計數器歸零，通常放在迴圈的開頭或結尾)
#    - write_file(filename="PracticeWrite.txt"): 文件寫入函數 (可以指定文件名稱，預設為 PracticeWrite.txt)
#    - close_file(file_handle): 關閉文件函數，用於結束文件寫入並恢復到標準輸出
# 4. 使用範例:
#    - 首先載入模組:
#      import sys
#      sys.path.append(r"G:\我的雲端硬碟\Python_Tool-main")
#      from GoodTool import print_step_calculator, reset_print_step, write_file, close_file, toggle_debug_mode
#    - 開啟調試模式:
#      toggle_debug_mode(True)
#    - 重置步驟計數器:
#      reset_print_step()
#    - 寫入文件:
#      file_handle = write_file("PracticeWrite.txt")
#    - 在迴圈或流程中，記錄每一步驟:
#      for i in range(5):
#          print(print_step_calculator(f"這是第 {i} 個測試"))
#    - 關閉文件:
#      close_file(file_handle)
# 
# 註: 本模組適合用於記錄程式運行步驟，尤其在進行除錯時可以方便追蹤程式邏輯和執行流程。

# 全域變數：步驟計數器與除錯模式狀態
global_print_step = 0
debug_mode = True  # 預設啟用調試模式

# 重置步驟計數器函數
def reset_print_step():
    global global_print_step
    global_print_step = 0  # 每次調用時將計數器重置為0

# 打印詳細步驟信息
def print_step_calculator(words):
    if not debug_mode:
        return ""  # 如果調試模式關閉，則不打印任何資訊
    
    global global_print_step
    global_print_step += 1
    if words == "":
        words = ""
    current_function = inspect.stack()[1][3]  # 取得當前呼叫的函數名稱
    formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 格式化當前時間
    return f"[目前程序 : {current_function}]\n#Step {global_print_step}.\n      time : {formatted_time}\n         {words}\n"

# 打印簡單步驟信息
def print_step_calculator_simple():
    if not debug_mode:
        return ""  # 如果調試模式關閉，則不打印任何資訊

    global global_print_step
    global_print_step += 1
    current_function = inspect.stack()[1][3]
    formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"目前程序 : [{current_function}]  #Step {global_print_step}."

# 切換調試模式
def toggle_debug_mode(state=True):
    global debug_mode
    debug_mode = state  # 控制是否開啟或關閉調試模式

# 文件寫入函數
def write_file(filename="PracticeWrite.txt"):
    # 重定向 stdout 到文件
    file_handle = open(filename, "w")
    sys.stdout = file_handle
    return file_handle

# 關閉文件函數
def close_file(file_handle):
    # 恢復 stdout 並關閉文件
    if file_handle:
        file_handle.close()
    sys.stdout = sys.__stdout__  # 恢復預設標準輸出
