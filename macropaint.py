from PIL import Image
import pyautogui
import time

from pynput.mouse import Listener, Button

"""img = Image.open("test.png").convert("RGB")
width, height = img.size"""

time.sleep(3)

for y in range(50):
    for x in range(50):
        pyautogui.click(200 + x * 20, 200 + y * 20)


def on_click(x, y, button, pressed):
    if pressed and button == Button.x2:
        print(x, y)
    elif pressed:
        print(button)

with Listener(on_click=on_click) as listener:
    listener.join()