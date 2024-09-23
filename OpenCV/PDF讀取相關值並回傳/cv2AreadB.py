import cv2
import sys
import numpy as np
import pyautogui  # 用於螢幕截圖
import time  # 用於時間控制

sys.path.append(r'G:\我的雲端硬碟\Python_Tool-main\OpenCV\PDF讀取相關值並回傳\20240919154257639_6.pdf')
from GoodTool import print_step_calculator

# 讀取目標圖片（你想要尋找的圖片）
print(print_step_calculator(), "開始讀取目標圖片")
image = cv2.imread(r'G:\我的雲端硬碟\Python_Tool-main\OpenCV\PDF讀取相關值並回傳\Snipaste_2024-09-20_10-18-49.png')

if image is None:
    print("Failed to load image")
    sys.exit()
else:
    print(print_step_calculator(), "目標圖片讀取成功")

# 定義預處理函數列表
def preprocess_image(image, method):
    if method == 'gray':
        print(print_step_calculator(), "將圖像轉換為灰階")
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif method == 'blur':
        print(print_step_calculator(), "將圖像模糊處理")
        return cv2.GaussianBlur(image, (5, 5), 0)
    elif method == 'edges':
        print(print_step_calculator(), "進行邊緣檢測")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)
    elif method == 'equalize_hist':
        print(print_step_calculator(), "進行直方圖均衡化")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(gray)
    else:
        return image

# 使用 SIFT 進行特徵匹配
def sift_feature_matching(image, screen_image):
    print(print_step_calculator(), "使用 SIFT 進行特徵匹配")
    sift = cv2.SIFT_create()

    # 找到圖像的特徵點和描述符
    kp1, des1 = sift.detectAndCompute(image, None)
    kp2, des2 = sift.detectAndCompute(screen_image, None)

    # 建立暴力匹配器
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # 匹配描述符
    matches = bf.match(des1, des2)

    # 根據匹配距離排序
    matches = sorted(matches, key=lambda x: x.distance)

    # 繪製匹配結果，使用 drawMatches 繪製匹配特徵點和線條
    result_image = cv2.drawMatches(image, kp1, screen_image, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return result_image, kp1, kp2, matches

# 循環執行影像處理，運行10秒
def run_for_duration(duration, interval):
    start_time = time.time()
    
    while time.time() - start_time < duration:
        print(print_step_calculator(), "開始擷取螢幕截圖")
        screenshot = pyautogui.screenshot()

        # 將 screenshot 轉換為 numpy 陣列（OpenCV 可識別的格式）
        print(print_step_calculator(), "將螢幕截圖轉換為 numpy 陣列")
        screen_image = np.array(screenshot)

        # 轉換顏色格式，從 RGB 轉換為 BGR（OpenCV 使用 BGR）
        print(print_step_calculator(), "將螢幕截圖轉換為 BGR 格式")
        screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)

        print(print_step_calculator(), "螢幕截圖擷取成功")

        preprocessing_methods = ['gray', 'blur', 'edges', 'equalize_hist']
        found = False

        # 先嘗試使用預處理和 matchTemplate
        for method in preprocessing_methods:
            print(print_step_calculator(), f"嘗試預處理方法: {method}")

            # 預處理目標圖片和螢幕截圖
            processed_image = preprocess_image(image, method)
            processed_screen_image = preprocess_image(screen_image, method)

            # 使用 matchTemplate 來尋找目標圖片
            print(print_step_calculator(), f"使用 matchTemplate 進行匹配 (方法: {method})")
            result = cv2.matchTemplate(processed_screen_image, processed_image, cv2.TM_CCOEFF_NORMED)

            # 設定匹配的閾值，值越接近1表示匹配越好
            threshold = 0.8
            loc = np.where(result >= threshold)

            # 如果找到匹配，畫出藍色框框
            if len(loc[0]) > 0:
                found = True
                print(print_step_calculator(), f"匹配成功，使用預處理方法: {method}")
                for pt in zip(*loc[::-1]):
                    start_point = pt  # 左上角座標
                    end_point = (pt[0] + image.shape[1], pt[1] + image.shape[0])  # 右下角座標
                    color = (255, 0, 0)  # 藍色 (BGR)
                    thickness = 2
                    cv2.rectangle(screen_image, start_point, end_point, color, thickness)
                break  # 找到後停止嘗試

            print(print_step_calculator(), f"未能匹配成功 (方法: {method})")

        # 如果 matchTemplate 找不到結果，使用 SIFT 進行特徵匹配
        if not found:
            print(print_step_calculator(), "未能找到匹配，嘗試使用 SIFT 進行特徵匹配")
            result_image, kp1, kp2, matches = sift_feature_matching(image, screen_image)

            # 繪製所有找到的關鍵點（在原圖和螢幕圖像上）
            matched_pts = []
            for match in matches[:10]:  # 繪製前10個匹配點
                img_idx = match.queryIdx
                scr_idx = match.trainIdx

                # 獲取在圖像和螢幕截圖上的座標
                img_pt = tuple(map(int, kp1[img_idx].pt))
                scr_pt = tuple(map(int, kp2[scr_idx].pt))
                matched_pts.append(scr_pt)  # 保存螢幕圖上的匹配點

                # 在螢幕截圖上畫出匹配的點 (圈圈)
                cv2.circle(screen_image, scr_pt, 10, (0, 255, 0), 3)  # 綠色圈圈代表匹配點

            # 如果有找到匹配點，畫出藍色框框
            if matched_pts:
                min_x = min([pt[0] for pt in matched_pts])
                min_y = min([pt[1] for pt in matched_pts])
                max_x = max([pt[0] for pt in matched_pts])
                max_y = max([pt[1] for pt in matched_pts])

                # 在螢幕上畫出藍色矩形框框
                cv2.rectangle(screen_image, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)  # 藍色框框

        # 顯示包含特徵點和匹配結果的螢幕圖片
        cv2.imshow('Detected keypoints and bounding box', screen_image)
        cv2.waitKey(1)  # 每次更新圖片

        # 等待 X 秒後繼續
        print(print_step_calculator(), f"等待 {interval} 秒後繼續")
        time.sleep(interval)

# 設置每 5 秒進行一次影像處理，並總共運行 10 秒
run_for_duration(10, 2)
