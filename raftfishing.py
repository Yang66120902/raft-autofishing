import time
import pyautogui
import cv2
import numpy as np
import keyboard

BUTTON_REGION = (1404, 912, 60, 60) #(x, y, width, height)

BRIGHTNESS_THRESHOLD = 100


resume = True


def capture_region(region):
    """
    截取屏幕指定区域并转换为灰度图
   
    """
    screenshot = pyautogui.screenshot(region=region)  # 截取屏幕区域
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)  # 转换为灰度图


def is_button_disappeared():
    """
    判断按钮是否消失（区域变黑）

    """
    img = capture_region(BUTTON_REGION)  # 截取按钮区域
    avg_brightness = np.mean(img)  # 计算该区域的平均亮度
    return avg_brightness < BRIGHTNESS_THRESHOLD  # 判断是否低于阈值（按钮消失）


def perform_mouse_action():
    """
    执行鼠标操作：
    1. 等待0.8s(raft上钩后有延迟)
    2. 按下0.3秒(收钩子)
    3. 松开0.6秒
    4. 按下2秒(蓄力出杆)
    5. 松开5秒(缓冲时间)
    """
    print("按钮消失，执行鼠标操作（掉到鱼了，自动收钩子再出钩）...")
    time.sleep(0.8)
    pyautogui.mouseDown()
    time.sleep(0.3) 
    pyautogui.mouseUp()
    time.sleep(0.6)

    pyautogui.mouseDown() 
    time.sleep(2)

    pyautogui.mouseUp()
    time.sleep(5)


    
def stop_script():
    """
    检测鼠标是否移动到左上角 (0,0) 来停止脚本
    """
    global resume
    x, y = pyautogui.position()  # 获取鼠标当前位置
    if x == 0 and y == 0:  
        print("鼠标移至左上角，脚本已暂停。（按 = 重新启动。）")
        resume = False


# 监听=键来重新启用脚本
def listen_for_resume():
    """
    监听键盘按键，按 = 重新启用脚本
    """
    global resume
    keyboard.wait("=")
    resume = True  # 重新启用检测
    print("钓鱼脚本已重启")
    

# 主循环
while True:
    if resume:  # 只有当 resume=True 时，才会执行检测
        stop_script()  # 检查是否需要停止脚本
        if is_button_disappeared():
            perform_mouse_action()
        time.sleep(0.5)  # 防止过快
    else:
        listen_for_resume()  # 等待按 = 重新开始自动钓鱼
