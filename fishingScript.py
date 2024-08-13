import time
import pyautogui
import cv2
from PIL import ImageGrab
import numpy as np

average=[0]

# Load float image in greyscale mode
floatGreyNp = cv2.imread('float.png', 0)
cv2.imwrite('greyFloat.png', floatGreyNp)
h, w = floatGreyNp.shape

# Perform 10 attempts
for k in range(1, 11):
    x=0
    y=0
    print('Attempt:', k, '/', 10)
    
    # Activate fishing skill
    pyautogui.press('2')
    time.sleep(2)

    # Take a screenshot and convert it to greyscale
    base_screen= ImageGrab.grab()
    base_screen.save('screenshot.png')
    screenshotGreyNp = cv2.imread('screenshot.png', 0)
        
    # Use normalized cross-correlation for template matching
    res = cv2.matchTemplate(screenshotGreyNp, floatGreyNp, cv2.TM_CCOEFF_NORMED)

    # Find locations where the correlation coefficient is above the threshold
    floatLocation= np.where(res >= 0.7)

    # Skip iteration if float was not found
    if not floatLocation[0].size:
        print('cant find the float')
        continue

    # Get the location of the first match
    for coordinates in zip(*floatLocation[::-1]):
            x = int(coordinates[0])
            y = int(coordinates[1])

    # Monitor the area around the detected float
    for h in range(0,20):
        # Capture the float picture from the screen
        capturedFloatGreyNp = ImageGrab.grab(bbox =(x, y, x + w, y + h)).convert('L')
        
        # Calculate the average pixel value of the captured float area
        mean = np.mean(capturedFloatGreyNp)

        # Find the difference between previously recorded average and the one that was jsut calculated
        # i.e. how different does the float area look like comparing to few moments ago(0.3 secs ago)
        diff = average[-1] - mean
        time.sleep(0.3)
        average.append(mean)

        # If the difference exceeds the threshold, a bait is detected
        if diff > 5:
            # Take the fish out and reset the position of cursor
            print('Bite detected!')
            pyautogui.moveTo(x + 5 , y + 5)
            pyautogui.keyDown('shift')
            pyautogui.click(button='right')
            pyautogui.mouseUp()
            pyautogui.keyUp('shift')
            pyautogui.moveTo(100, 100)
            success +=1
            break   
    
    #null the info after iteration
    try:
        del(x)
        del(y)
    except:
        pass
    average= [0]
