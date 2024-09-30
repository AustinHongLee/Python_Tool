def string_working_process_in():
    # 探討 Python 中的字串運作邏輯

    # 定義一個字串變數 str1，值為 "apple"
    str1 = "apple"

    # 在 Python 的底層，字串可以視作一個字符列表
    # 例如 str1 = "apple" 可以被理解為 ["a", "p", "p", "l", "e"]
    py_look_str1 = ["a", "p", "p", "l", "e"]

    # 打印字串中第三個字符的例子，使用索引 [2]
    print(f"str1 的第三個字符: {str1[2]}")
    print(f"py_look_str1 的第三個值: {py_look_str1[2]}")

    # 比較字串和字符列表中相同索引處的值
    try:
        if str1[2] == py_look_str1[2]:
            print("兩者在索引 2 處的值相同，結果為 True")
    except Exception as e:
        print(f"出錯了: {e}")

    # 模擬 VBA 的 left() 或 right() 函數
    # 在 Python 中，使用切片來實現類似功能，格式為 [start:end:step]

    # 例子：模擬 VBA 的 left(str1, 2)，即從左邊取出兩個字符
    print("模擬 VBA 的 <<left(str1, 2)>>")
    temp_ques = str1[0:2]
    print(f"結果: [{temp_ques}]")

    # 為什麼使用 [0:2]？
    # 理論上，索引 [0] 對應 "a", [1] 對應 "p", [2] 對應 "p"
    # 但切片的定義是 [start:end-1]，因此實際取到的是前兩個字符，結果為 "ap"

    # 切片的概念是：從 start 索引開始，取到 end 索引之前的值
    # 例如 [0:2] 代表取從索引 0 到索引 1 的值，總長度為 2
    # 因此 len([0:2-1]) = 2

    # 例子：模擬 VBA 的 right(str1, 2)，即從右邊取出兩個字符
    print("模擬 VBA 的 <<right(str1, 2)>>")
    temp_ques = str1[-2:]
    print(f"結果: [{temp_ques}]")

    # 例子：模擬 VBA 的 mid(str1,2,2)，即從左數到第二字元為開始, 輸出兩個字元後結束。
    print("模擬 VBA 的 <<mid(str1, 2, 2)>>")
    temp_start = 1
    temp_len = 2
    temp_ques = str1[temp_start:1+temp_len]
    print(f"結果: [{temp_ques}]")

    # 例子: 模擬 VBA 的 Replace(字串, 搜尋文字, 替換文字[, 起始位置[, 替換次數[, 比對方式]]])
    print('模擬VBA的 <<replace(str1, "p", "d")>>')
    temp_old = "p"
    temp_new = "d"
    temp_ques = str1.replace(temp_old, temp_new,1)
    print(f"結果: [{temp_ques}]")

    # 例子：模擬 VBA 的 InStr([start], string1, string2, [compare]) or 可以說是內建函數find
    print('模擬 VBA 的 InStr(1,str1,"p")')
    temp_find_word = "p"
    temp_ques = str1.find(temp_find_word,0)
    print(f"結果: [{temp_ques}]")

    # 例子 : 模擬VBA 的Trim("字串") attention : 與VBA相同, 只能對於<start> and <end> 部分 即是兩端的空白做刪除
    print('模擬 VBA的 Trim(str1)')
    temp_str1 = "   " +str1 + "   "
    print(f"Now let str1 join some space in here : {temp_str1}")
    print(f"Start to trim temp_str1")
    print(f"{temp_str1.strip()}")
    # 延伸此問題可能之問題
    print("延伸問題:")
    temp_str2 = str1 + "    " + "<end>"
    print(f"Now let str1 join some space in middle : {temp_str2}")
    print(f"Start to trim temp_str2")
    temp_str2_box = temp_str2.strip()
    temp_len = len(str1)
    if temp_str2_box[temp_len:temp_len+5] == "<end>":
        print(f"確定刪除{temp_str2_box}")
    else:
        print(f"刪除失敗{temp_str2_box}")
    # Use <VBA> substitute like the function <python> replace to trim the middle space
    temp_str2_box = temp_str2.replace(" ","")
    if temp_str2_box[temp_len:temp_len+5] == "<end>":
        print(f"確定刪除{temp_str2_box}")
    else:
        print(f"刪除失敗{temp_str2_box}")

    # 例子 : 模擬VBA 的TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)
    temp_str1 = "_".join(str1)
    print(f"insert delimiter in string {temp_str1}")
    # 延伸可能情況 : 可能會出現 str1 = "ap ple "
    # 如果不做排解會如下:
    temp_str1 = "ap ple "
    print(f"some how maybe have this problem like this {temp_str1} middle space and end space in this word")
    print(f"insert delimiter in string {"_".join(temp_str1)}") # a_p_ _p_l_e_
    # 需做預處理 first step
    print(f"First step we need use replace() or strip()")
    temp_str1 = temp_str1.replace(" ","")
    print(f"insert delimiter in string {"_".join(temp_str1)}")


if __name__ == "__main__":
    string_working_process_in()
