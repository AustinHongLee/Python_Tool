import os
import sys
sys.path.append(r'G:\我的雲端硬碟\Python_Tool-main\\')
from GoodTool import print_step_calculator, reset_print_step, toggle_debug_mode, write_file, close_file

def main():
    # 启动调试模式并重置步骤计数器
    toggle_debug_mode(True)  # 开启调试模式
    reset_print_step()       # 重置计数器
    for i in range(0:5):
        print("HO" + print_step_calculator())
    # 关闭调试模式
    
    