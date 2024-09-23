import sys
import datetime
import inspect

# Global print step counter
global_print_step = 0
debug_mode = True  # 默认开启调试模式

# 重置计数器函数
def reset_print_step():
    global global_print_step
    global_print_step = 0  # 每次调用时将计数器重置为0

# 打印详细步骤信息
def print_step_calculator(words):
    if not debug_mode:
        return ""  # 如果调试模式关闭，则不打印任何信息
    
    global global_print_step
    global_print_step += 1
    if words == "":
        words = ""
    current_function = inspect.stack()[1][3]
    formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[目前程序 : {current_function}]\n#Step {global_print_step}.\n      time : {formatted_time}\n         {words}\n"

# 打印简单步骤信息
def print_step_calculator_simple():
    if not debug_mode:
        return ""  # 如果调试模式关闭，则不打印任何信息

    global global_print_step
    global_print_step += 1
    current_function = inspect.stack()[1][3]
    formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"目前程序 : [{current_function}]  #Step {global_print_step}."

# 切换调试模式函数
def toggle_debug_mode(state=True):
    global debug_mode
    debug_mode = state  # 控制是否开启或关闭调试模式

# 文件写入函数
def write_file(filename="PracticeWrite.txt"):
    # 重定向 stdout 到文件
    file_handle = open(filename, "w")
    sys.stdout = file_handle
    return file_handle

# 关闭文件函数
def close_file(file_handle):
    # 恢复 stdout 并关闭文件
    if file_handle:
        file_handle.close()
    sys.stdout = sys.__stdout__  # 恢复默认标准输出
