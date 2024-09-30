import fitz  # PyMuPDF
import os
import sys
sys.path.append(r"G:\我的雲端硬碟\Python_Tool-main")
from GoodTool import print_step_calculator

directory = os.path.dirname(__file__)  # 獲取當前文件所在的目錄
pdf_name = "Testing_Catch.pdf"
pdf_path = os.path.join(directory, pdf_name)  # PDF 文件的完整路徑

# Try to open the pdf file and catch freetext attributes
def catching_machine(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # 加載第0頁
    annot = page.first_annot  # 獲取第一個註解
    if annot and annot.type[0] == 2:  # 8 是 FreeTextCallout 標註類型
        print(print_step_calculator("找到 FreeTextCallout 標註"))
        return

    xref = annot.xref  # 獲取註解的 xref
    stream_data = doc.xref_stream(xref)  # 讀取 xref 流

    # 檢查 xref 流是否為 None
    if stream_data is None:
        print("該 xref 沒有可用的流數據")
        return

    # 獲取 xref 原內容資訊，手動查找 /Contents 部分
    if "/Contents" not in stream_data:
        print("未找到 Contents 部分")
        return

    updated_content = "This is a test"
    # 修改 Contents 部分，這裡替換舊的文本
    new_stream_data = stream_data.replace("/Contents (Hello:D!python)", f"/Contents ({updated_content})")
    doc.update_stream(xref, new_stream_data)  # 寫回修改後的流

    # 重新生成外觀流以保留箭頭和邊框
    annot.update()

    # 保存修改後的文件
    updated_pdf_path = os.path.join(directory, "updated_file.pdf")
    doc.save(updated_pdf_path)
    doc.close()

    print(f"更新後的文件已保存到 {updated_pdf_path}")

def main():
    catching_machine(pdf_path)
    print(print_step_calculator("程序執行完畢！"))

if __name__ == "__main__":
    main()
