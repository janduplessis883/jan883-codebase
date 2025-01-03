import pyautogui

# Get the size of the primary monitor
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

# Move the mouse to (136, 270) and click twice
pyautogui.moveTo(136, 270, duration=2)
pyautogui.click(x=136, y=270, clicks=2, interval=0.5, button='left')

# Move to a new position (528, 370) and click
pyautogui.moveTo(528, 370, duration=2)
pyautogui.click(button='left')

# Type email with a slight delay between each character
pyautogui.write('drjanduplessis@icloud.com', interval=0.1)

# Taking and saving a screenshot
pyautogui.screenshot('my_screenshot.png')

# Optional: Show the screenshot object
img = pyautogui.screenshot()
img.show()

# Locate an image on the screen
location = pyautogui.locateOnScreen('this.png')
if location:
    print("Image found at", location)
else:
    print("Image not found")

# Show an alert box
pyautogui.alert(text='Operation complete', title='Alert', button='OK')
