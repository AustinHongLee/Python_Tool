from itertools import combinations
import os
import sys
import datetime

# 設定當前時間格式化
formatted_time = datetime.datetime.now().strftime('%Y-%m-%d')

# 設定當前腳本的路徑
dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\"  # 添加斜線確保路徑正確

# 將 GoodTool 模塊加入路徑中
sys.path.append(r'G:\我的雲端硬碟\Python_Tool-main\\')

# 從 GoodTool 中導入函數
from GoodTool import print_step_calculator, reset_print_step, toggle_debug_mode, write_file, close_file

# 開啟調試模式
toggle_debug_mode(True)

# 輸入的管線長度列表
pipe_needs = [1254, 3378, 4155, 6789, 6522, 10223, 850, 3320, 8652]  # 這是所需的管線長度
pipe_length = 6000  # 這是可用的單一管線的標準長度

# 管線長度計算函數
def calculate_pipe_usage(pipe_needs, pipe_length):
    # 將管線需求按降序排列，以最大化使用效率
    pipe_needs.sort(reverse=True)  # 排序
    print(print_step_calculator(f"排序後的管線需求: {pipe_needs}"))  # 打印排序後的管線需求
    
    used_pipes = []  # 存儲每根管線的使用情況

    while pipe_needs:
        current_pipe = []  # 當前正在使用的管線中的片段
        remaining_length = pipe_length  # 當前管線剩餘的可用長度
        print(print_step_calculator(f"開始新的管線，長度為: {pipe_length}"))
        print(print_step_calculator(f"剩餘的管線需求: {pipe_needs}"))

        # 嘗試將盡可能多的管段放入當前管線中
        for length in pipe_needs[:]:
            if length <= remaining_length:
                current_pipe.append(length)
                remaining_length -= length
                pipe_needs.remove(length)
                print(print_step_calculator(f"將 {length} mm 添加到當前管線中。剩餘長度: {remaining_length} mm"))

        if current_pipe:
            used_pipes.append(current_pipe)
            print(print_step_calculator(f"當前管線完成: {current_pipe}"))

        # 處理超出管線長度的需求
        for length in pipe_needs[:]:
            if length > pipe_length:
                print(print_step_calculator(f"處理長度 {length} mm，超過管線長度 {pipe_length} mm"))
                pipe_needs.remove(length)
                full_pipes = length // pipe_length
                remainder = length % pipe_length
                for _ in range(full_pipes):
                    used_pipes.append([pipe_length])
                    print(print_step_calculator(f"使用完整的管線，長度為 {pipe_length} mm"))
                if remainder > 0:
                    pipe_needs.append(remainder)
                    print(print_step_calculator(f"剩餘的 {remainder} mm 被重新添加到需求中"))
    
    return used_pipes  # 返回已使用的管線列表

# 開始文件寫入
file_handle = write_file(f"{dir_path}管線使用結果_{formatted_time}.txt")  # 打開文件進行寫入

# 計算最佳使用方式
optimal_pipe_usage = calculate_pipe_usage(pipe_needs, pipe_length)

# 顯示結果並寫入文件
print("\n最佳管線使用方式:")
for i, pipe in enumerate(optimal_pipe_usage, 1):
    print(f"管線 {i}: {' + '.join(map(str, pipe))} = {sum(pipe)} mm")

# 關閉文件寫入
close_file(file_handle)

# 重置計數器
reset_print_step()
