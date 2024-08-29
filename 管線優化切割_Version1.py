from itertools import combinations

# 輸入的管線長度列表
pipe_needs = [1254, 3378, 4155, 6789]  # 這是所需的管線長度
pipe_length = 6000  # 這是可用的單一管線的標準長度

# 計算最佳管線使用方式的函數
def calculate_pipe_usage(pipe_needs, pipe_length):
    # 將管線需求按降序排列，以最大化使用效率
    pipe_needs.sort(reverse=True)  # 先對需求進行排序，從最大需求開始，便於優先處理大長度
    # .sort() 方法會直接修改原始列表，不會返回新的列表
    # 如果需要保留原始列表，可以使用 sorted() 函數
    # pipe_needs = sorted(pipe_needs, reverse=True)
    # 利用reverse=True參數，可以將列表進行反向排序，即從大到小排序
    print("排序後的管線需求:", pipe_needs)
    used_pipes = []  # 這裡存儲每根管線的使用情況
    
    while pipe_needs:
        current_pipe = []  # 當前正在使用的管線中的片段
        remaining_length = pipe_length  # 當前管線剩餘的可用長度
        
        print("\n開始新的管線，長度為:", pipe_length)
        print("剩餘的管線需求:", pipe_needs)
        
        # 嘗試將盡可能多的管段放入當前管線中
        for length in pipe_needs[:]:  # 遍歷管線需求列表
            if length <= remaining_length:  # 如果這段長度可以放入當前管線中
                current_pipe.append(length)  # 將這段長度加入當前管線
                remaining_length -= length  # 減少剩餘可用長度
                pipe_needs.remove(length)  # 從需求列表中移除已使用的長度
                print(f"將 {length} mm添加到當前管線中。剩餘長度: {remaining_length} mm")
        
        if current_pipe:  # 只有當前管線有內容時才將其加入已使用的管線列表
            used_pipes.append(current_pipe)  # 將當前使用的管線添加到已使用管線列表中
            print("當前管線完成:", current_pipe)
        
        # 處理超過可用管線長度的需求
        for length in pipe_needs[:]:  # 再次遍歷剩餘的需求
            if length > pipe_length:  # 如果需求長度超過可用管線的長度
                print(f"\n處理長度 {length} mm，超過管線長度 {pipe_length} mm")
                pipe_needs.remove(length)  # 從需求列表中移除這段長度
                # 將長度分割為完整的管線和剩餘部分
                full_pipes = length // pipe_length  # 計算需要多少根完整的管線
                remainder = length % pipe_length  # 計算剩餘部分的長度
                for _ in range(full_pipes):
                    used_pipes.append([pipe_length])  # 添加完整的管線到使用列表中
                    print(f"使用完整的管線，長度為 {pipe_length} mm")
                if remainder > 0:  # 如果還有剩餘部分
                    pipe_needs.append(remainder)  # 將剩餘的部分重新添加到需求列表中
                    print(f"剩餘的 {remainder} mm被重新添加到需求中")
    
    return used_pipes  # 返回已使用的管線列表

# 計算最佳使用方式
optimal_pipe_usage = calculate_pipe_usage(pipe_needs, pipe_length)

# 顯示結果
print("\n最佳管線使用方式:")
for i, pipe in enumerate(optimal_pipe_usage, 1):
    print(f"管線 {i}: {' + '.join(map(str, pipe))} = {sum(pipe)} mm")
