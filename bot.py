import time
import pyautogui
import cv2
from PIL import ImageGrab
import numpy as np

average=[0,]

template = cv2.imread('template.png', 0)
w, h = template.shape[::-1]

for _ in range(100):
    
    # move mouse and click on fishing
    time.sleep(1)
    pyautogui.moveTo(240,710)
    time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.4)
    pyautogui.mouseUp()
    time.sleep(3)
    
    #cut out the focus area and transmog it
    base_screen= ImageGrab.grab(bbox =(0,0,800,450))
    base_screen.save('///Wow fishing bot/base_screen.png')
    img_rgb = cv2.imread('base_screen.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    #compare images
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc= np.where(res >=0.7)
    
    for i in range(40):
        
        try:
           
            clean_screen = ImageGrab.grab(bbox =(x,y,x+w,y+h))
            mean = np.mean(clean_screen)
            diff = average[-1] - mean
            print(diff)
            
            # taking poplavok out
            if 1<= diff:
                
                pyautogui.moveTo(x+15 , y+15 )
                print('waiting to cath')
                pyautogui.click(button='right') 
                time.sleep(2)
                pyautogui.mouseUp()
                break
            average.append(mean)
                
        except:
            #location of bait
            print('cant find the small image')
            for pt in zip(*loc[::-1]):
                x = int(pt[0])
                y = int(pt[1])
            time.sleep(0.2)
     
    #null the info after iteration
    pyautogui.moveTo(400,400)
    try:
        del(x)
        del(y)
    except:
        pass
    average= [0]
