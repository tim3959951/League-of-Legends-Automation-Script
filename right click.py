import pyautogui
import random
import time

def right_click_random_position():
    #get screen size
    screen_width, screen_height = pyautogui.size()
    
    # random cooridinate
    x = random.randint(0, screen_width - 10)
    y = random.randint(0, screen_height - 10)
    
    # move to random position
    pyautogui.moveTo(x, y, duration=1)
    
    # right click
    pyautogui.click(button='right')

if __name__ == "__main__":
    while True:
        right_click_random_position()
        time.sleep(1)
