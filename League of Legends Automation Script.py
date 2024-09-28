import cv2
import numpy as np
import pyautogui
import time
import random

def right_click_random_position():
    screen_width, screen_height = pyautogui.size()
    x = random.randint(0, screen_width - 10)
    y = random.randint(0, screen_height - 10)
    pyautogui.moveTo(x, y, duration=1)
    pyautogui.click(button='right')

def find_and_click(icons_paths, threshold=0.8):
    sup_clicked = False
    yumi_clicked = False
    can_click_lock = False  
    keep_running = False  
    last_clicked_times = {}  
    cooldown = 5  

    while True:
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        for icon_path in icons_paths:
            if 'lock.png' in icon_path:
                continue  # Skip lock processing in the main loop
            icon = cv2.imread(icon_path, 0)
            if icon is None:
                print(f"Error loading image: {icon_path}")
                continue

            res = cv2.matchTemplate(screen_gray, icon, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                icon_name = icon_path.split('/')[-1]
                logical_x = (pt[0] + icon.shape[1]//2) // 2
                logical_y = (pt[1] + icon.shape[0]//2) // 2
                current_time = time.time()

                if icon_name in last_clicked_times and current_time - last_clicked_times[icon_name] < cooldown:
                    print(f"{icon_name} is still in cooldown.")
                    continue

                pyautogui.moveTo(logical_x, logical_y, duration=0.5)
                pyautogui.click(button='left')
                last_clicked_times[icon_name] = current_time

                #if icon_path.endswith('sup1.png'):
                 #   sup_clicked = True
                if icon_path.endswith('yumi1.png'):
                    yumi_clicked = True
                    # Stop right click random position if "one more game" or "find match" is clicked
                if icon_path.endswith('continue.png') or icon_path.endswith('next.png') or icon_path.endswith('ok.png'):
                    keep_running = False

        if yumi_clicked :
            # Now check for lock.png
            lock_res = cv2.matchTemplate(screen_gray, cv2.imread('/Users/tim/Desktop/lock.png', 0), cv2.TM_CCOEFF_NORMED)
            if np.max(lock_res) >= 0.8:
                lock_loc = np.where(lock_res >= 0.8)
                for pt in zip(*lock_loc[::-1]):
                    logical_x = (pt[0] + icon.shape[1] // 2)//2
                    logical_y = (pt[1] + icon.shape[0] // 2)//2
                    pyautogui.moveTo(logical_x, logical_y, duration=0.5)
                    pyautogui.click(button='left')
                    print(f"Clicked lock.png at ({logical_x}, {logical_y}) wait 10 sec for right click")
                    #sup_clicked = False
                    yumi_clicked = False
                    time.sleep(30)
                    keep_running = True  # Reset conditions and continue if needed
                    

        if keep_running:
            right_click_random_position()
            


        # Optional sleep to reduce CPU usage, uncomment if necessary
        # time.sleep(1) 

icons_paths = [
    '/Users/tim/Desktop/one more game.png',
    '/Users/tim/Desktop/continue.png',
    '/Users/tim/Desktop/find match1.png',
    '/Users/tim/Desktop/find match.png',
   # '/Users/tim/Desktop/sup1.png',
    '/Users/tim/Desktop/yumi1.png',
    '/Users/tim/Desktop/lock.png',
    '/Users/tim/Desktop/finish game.png',
    '/Users/tim/Desktop/next.png',
    '/Users/tim/Desktop/accept match.png',
    '/Users/tim/Desktop/ok.png',
]
find_and_click(icons_paths)
