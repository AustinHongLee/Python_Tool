import turtle as t
# 龜形繪圖參數設定
'''
龜的運動
移動與繪圖：
forward() | fd()  # 向前移動
backward() | bk() | back()  # 向後移動
right() | rt()  # 向右轉
left() | lt()  # 向左轉
goto() | setpos() | setposition()  # 移動到指定位置
teleport()  # 瞬間移動（非標準turtle函式）
setx()  # 設定X座標
sety()  # 設定Y座標
setheading() | seth()  # 設定前進方向
home()  # 回到原點
circle()  # 繪製圓形
dot()  # 繪製點
stamp()  # 龜的形狀蓋印
clearstamp()  # 刪除指定印章
clearstamps()  # 刪除所有印章
undo()  # 撤銷上一步動作
speed()  # 設定速度

告知龜的狀態：
position() | pos()  # 回傳目前座標位置
towards()  # 計算方向
xcor()  # 回傳X座標
ycor()  # 回傳Y座標
heading()  # 回傳目前前進方向
distance()  # 計算與某位置的距離

設定與測量：
degrees()  # 設定角度單位為度數
radians()  # 設定角度單位為弧度

畫筆控制：
繪圖狀態：
pendown() | pd() | down()  # 放下畫筆（開始繪圖）
penup() | pu() | up()  # 提起畫筆（停止繪圖）
pensize() | width()  # 設定畫筆粗細
pen()  # 設定畫筆屬性
isdown()  # 檢查畫筆是否放下

顏色控制：
color()  # 設定畫筆和填充顏色
pencolor()  # 設定畫筆顏色
fillcolor()  # 設定填充顏色

填充控制：
filling()  # 檢查是否正在填充
begin_fill()  # 開始填充
end_fill()  # 結束填充

更多繪圖控制：
reset()  # 重置畫面
clear()  # 清除繪圖
write()  # 在畫布上寫文字

龜的狀態：
可見性：
showturtle() | st()  # 顯示龜
hideturtle() | ht()  # 隱藏龜
isvisible()  # 檢查龜是否可見

外觀設定：
shape()  # 設定龜的形狀
resizemode()  # 設定縮放模式
shapesize() | turtlesize()  # 設定龜的大小
shearfactor()  # 設定剪切角度
settiltangle()  # 設定傾斜角度
tiltangle()  # 回傳傾斜角度
tilt()  # 傾斜龜的形狀
shapetransform()  # 設定形狀變換
get_shapepoly()  # 回傳多邊形的頂點

使用事件：
onclick()  # 點擊事件
onrelease()  # 鬆開點擊事件
ondrag()  # 拖動事件

特殊的龜方法：
begin_poly()  # 開始多邊形繪製
end_poly()  # 結束多邊形繪製
get_poly()  # 獲取多邊形數據
clone()  # 複製龜
getturtle() | getpen()  # 獲取當前的龜
getscreen()  # 獲取屏幕對象
setundobuffer()  # 設置撤銷緩衝區
undobufferentries()  # 撤銷緩衝區條目

TurtleScreen/Screen的方法：
視窗控制：
bgcolor()  # 設定背景顏色
bgpic()  # 設定背景圖片
clearscreen()  # 清除屏幕
resetscreen()  # 重置屏幕
screensize()  # 設定屏幕大小
setworldcoordinates()  # 設定世界坐標

動畫控制：
delay()  # 設定動畫延遲
tracer()  # 設定繪圖更新速率
update()  # 手動更新屏幕

使用屏幕事件：
listen()  # 開啟事件監聽
onkey() | onkeyrelease()  # 鍵盤按鍵事件
onkeypress()  # 鍵盤按下事件
onclick() | onscreenclick()  # 點擊屏幕事件
ontimer()  # 設置計時器事件
mainloop() | done()  # 開始事件循環

設定和特殊方法：
mode()  # 設定畫布模式
colormode()  # 設定顏色模式
getcanvas()  # 獲取畫布對象
getshapes()  # 獲取形狀列表
register_shape() | addshape()  # 註冊自定義形狀
turtles()  # 獲取當前所有龜的列表
window_height()  # 獲取視窗高度
window_width()  # 獲取視窗寬度

輸入方法：
textinput()  # 獲取文字輸入
numinput()  # 獲取數字輸入

Screen專屬的方法：
bye()  # 關閉窗口
exitonclick()  # 點擊離開
setup()  # 設定畫布尺寸
title()  # 設定窗口標題
'''

# 設定畫筆速度和顏色
t.speed(3)
t.pencolor("black")

# 開始繪製字母 "a"
t.penup()  # 提起畫筆，不繪圖
t.goto(-50, 0)  # 移動到起始位置
t.pendown()  # 放下畫筆，開始繪圖

t.circle(25)  # 畫出字母"a"的圓形部分

t.penup()
t.goto(-25, 0)  # 移動到 "a" 的右側下方
t.pendown()

t.left(90)  # 向上轉90度
t.forward(50)  # 向上畫一條直線，形成"a"的垂直部分

# 完成繪製，保持視窗打開
t.hideturtle()  # 隱藏畫筆圖案
t.done()  # 完成繪圖，等待窗口關閉
