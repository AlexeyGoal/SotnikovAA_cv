import numpy as np 
import pyautogui as pg 
import mss 
import keyboard 


screen_width = pg.size().width

i = 1 
widht = 80
max_w = 345
screen = {'top':350, 'left': 665, 'width': widht, 'height': 25}
sct = mss.mss()
''''
def find_dino_by_template(template_path, threshold=0.8):
    # Загрузка шаблона
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)               
    
    
    # Получаем скриншот экрана
    with mss.mss() as sct:
        screenshot = np.array(sct.grab({
            'top': 0,
            'left': 0,
            'width': pg.size().width,                   
            'height': pg.size().height
        }))
            
    # Конвертируем в RGB (OpenCV использует BGR)
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
    
    # Поиск шаблона
    result = cv2.matchTemplate(screenshot_rgb, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Проверка порога совпадения         
    if max_val >= threshold:
        # Возвращаем центр найденной области
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    
    return None'''

while True:
    image= np.array(sct.grab(screen))
            
    if image.mean() < 249:
                
        pg.press('space')
                                                               
    if widht < max_w:
        i += 1                   
        if i == 100:
            widht += 3
            screen = {'top':350, 'left': 665, 'width': widht, 'height': 25}
            i = 1 
                    
    if keyboard.is_pressed('q'):
        print("break")
        break        
         
        
        
        
