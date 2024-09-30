import os
import sys
sys.path.append(r"G:\我的雲端硬碟\Python_Tool-main")
from GoodTool import print_step_calculator, reset_print_step, write_file, close_file, toggle_debug_mode

def main ():
    # First step is try to find the directory
    directory_now = r"G:\我的雲端硬碟\Python_Tool-main"
    # Then got this list all data detail :D
    for root, dirs, files in os.walk(directory_now):
        if root != "*.git*":
            print(print_step_calculator(f"This data root:{root}\n         dirs:{dirs}\n         files:{files}"))
            str1 = "apple pie apple tart apple cake"
            print(print_step_calculator(len(str1)))

if __name__ == '__main__':
    main()

