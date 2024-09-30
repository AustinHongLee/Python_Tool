import os
import sys
sys.path.append(r"G:\我的雲端硬碟\Python_Tool-main")
from GoodTool import print_step_calculator, reset_print_step, write_file, close_file, toggle_debug_mode


def system_info():
    # 1. 獲取當前工作目錄
    current_directory = os.getcwd()
    print(print_step_calculator("當前工作目錄：\n{current_directory}\n"))

    # 2. 列出當前目錄中的文件和資料夾
    directory_content = os.listdir()
    print(print_step_calculator("目錄內容：\n{directory_content}\n"))

    # 3. 檢查一個特定文件或資料夾是否存在
    file_name = 'example.txt'  # 可以修改為你想檢查的文件
    if os.path.exists(file_name):
        print(print_step_calculator("{file_name} 存在。\n"))
    else:
        print(print_step_calculator("{file_name} 不存在。\n"))

    # 4. 獲取指定文件的大小和最後修改時間
    if os.path.exists(file_name):
        file_size = os.path.getsize(file_name)
        mod_time = os.path.getmtime(file_name)
        print(f"{file_name} 的大小：{file_size} bytes")
        print(f"{file_name} 最後修改時間：{mod_time}\n")

    # 5. 創建新資料夾
    new_folder = 'new_folder'
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
        print(f"創建新資料夾：{new_folder}\n")
    else:
        print(f"資料夾 {new_folder} 已存在，無需創建。\n")

    # 6. 重命名文件或資料夾
    if os.path.exists(new_folder):
        os.rename(new_folder, 'renamed_folder')
        print(f"資料夾 {new_folder} 已重命名為 renamed_folder。\n")

    # 7. 執行一個簡單的系統命令
    os.system('echo Hello from Python!')

    # 8. 獲取環境變量
    path_env = os.getenv('PATH')
    print(f"PATH 環境變量：\n{path_env}\n")

    # 9. 遍歷某個目錄下的所有子目錄和文件
    for root, dirs, files in os.walk(current_directory):
        print(f"根目錄：{root}")
        print(f"資料夾：{dirs}")
        print(f"文件：{files}\n")
        # 避免列出過多內容，僅顯示當前目錄的內容
        break


# 呼叫函數來顯示系統資訊
system_info()
