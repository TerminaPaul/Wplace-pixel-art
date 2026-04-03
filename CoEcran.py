from pynput.mouse import Listener, Button
import pyperclip

def on_click(x, y, button, pressed):
    if pressed and button == Button.x2:
        print(x, y)
        pyperclip.copy(f"x={x}, y={y}")
    elif pressed:
        print(button)

with Listener(on_click=on_click) as listener:
    listener.join()