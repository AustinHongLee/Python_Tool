import cv2
import sys
import numpy as np
import fitz  # PyMuPDF, used for PDF image extraction
import screeninfo
import pytesseract  # 用於圖像識別 (OCR)

# 設定 Tesseract 的路徑 (依據你的 Tesseract 安裝位置)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\a0976\Downloads\tesseract-main\tesseract-main'

sys.path.append(r"G:\我的雲端硬碟\Python_Tool-main")
from GoodTool import print_step_calculator

# 讀取目標圖片（B.jpg）
print(print_step_calculator("讀取目標圖片"))
target_image = cv2.imread(r'C:\Users\a0976\Desktop\Hey.png')

if target_image is None:
    print("Failed to load target image")
    sys.exit()


# PDF 圖片提取函數
def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_np = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            images.append(image)
    return images


# 提取 PDF 中的所有圖片（A.pdf）
print(print_step_calculator("提取 PDF 中的圖片"))
pdf_images = extract_images_from_pdf(r'C:\Users\a0976\Desktop\4.XG32-3000A-BW-0656-01.pdf')

if not pdf_images:
    print("No images found in the PDF")
    sys.exit()


# 預處理圖片：轉換為灰度圖
def preprocess_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# 使用 SIFT 進行特徵匹配
def sift_feature_matching(target, source):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(target, None)
    kp2, des2 = sift.detectAndCompute(source, None)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    return kp1, kp2, matches


# 在 PDF 圖片中找到與 B.jpg 相似的內容
for idx, pdf_image in enumerate(pdf_images):
    print(print_step_calculator(f"處理第 {idx + 1} 頁圖片"))

    # 預處理 PDF 和目標圖片
    preprocessed_target = preprocess_image(target_image)
    preprocessed_pdf_image = preprocess_image(pdf_image)

    # 嘗試 SIFT 特徵匹配
    kp1, kp2, matches = sift_feature_matching(preprocessed_target, preprocessed_pdf_image)  # 使用返回的 kp1 和 kp2
    if matches:
        print(f"SIFT 特徵匹配成功，找到相似圖片在第 {idx + 1} 頁")
        for match in matches[:10]:
            img_idx = match.queryIdx
            scr_idx = match.trainIdx

            # 使用 kp1 和 kp2
            img_pt = tuple(map(int, kp1[img_idx].pt))
            scr_pt = tuple(map(int, kp2[scr_idx].pt))

            # 畫一個比匹配點稍大的矩形
            rect_size = 20  # 定義矩形擴大的大小
            start_point = (max(scr_pt[0] - rect_size, 0), max(scr_pt[1] - rect_size, 0))
            end_point = (min(scr_pt[0] + rect_size, pdf_image.shape[1]), min(scr_pt[1] + rect_size, pdf_image.shape[0]))

            # 繪製擴大的矩形
            cv2.rectangle(pdf_image, start_point, end_point, (255, 0, 0), 2)

            # 從矩形區域擷取圖像，用於 OCR 識別
            cropped_image = pdf_image[start_point[1]:end_point[1], start_point[0]:end_point[0]]

            # 使用 Tesseract 進行 OCR 識別
            text = pytesseract.image_to_string(cropped_image, config='--psm 6 digits')
            print(f"識別到的數字: {text.strip()}")

        break

# 取得螢幕的寬高
screen = screeninfo.get_monitors()[0]
screen_width, screen_height = screen.width, screen.height

# 根據螢幕大小縮放圖片
scale_factor = min(screen_width / pdf_image.shape[1], screen_height / pdf_image.shape[0])
new_width = int(pdf_image.shape[1] * scale_factor / 0.85)
new_height = int(pdf_image.shape[0] * scale_factor / 0.85)

# 調整圖片大小並旋轉
resized_image = cv2.resize(pdf_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
rotated_image = cv2.rotate(resized_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

# 顯示結果圖片
cv2.imshow('Matching Result', rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
