import cv2
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_EXPOSURE, -4)

glasses = cv2.imread("deal-with-it.png", cv2.IMREAD_UNCHANGED)

face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


eye_params = {
    'scaleFactor': 1.1,
    'minNeighbors': 8,
    'minSize': (30, 30),
    'maxSize': (100, 100)
}

def apply_glasses(frame, eyes):
    if len(eyes) >= 2:

        eyes = sorted(eyes, key=lambda x: x[0])
        
        eye1, eye2 = eyes[0], eyes[1]
        
        center_x = (eye1[0] + eye1[2]//2 + eye2[0] + eye2[2]//2) // 2
        center_y = (eye1[1] + eye1[3]//2 + eye2[1] + eye2[3]//2) // 2
        
        glasses_width = int(1.5 * abs((eye2[0] + eye2[2]//2) - (eye1[0] + eye1[2]//2)))
        glasses_height = int(glasses_width * glasses.shape[0] / glasses.shape[1])
        
        
        x1 = center_x - glasses_width//2
        x2 = x1 + glasses_width
        y1 = center_y - glasses_height//3  
        y2 = y1 + glasses_height
        
        
        if x1 >= 0 and y1 >= 0 and x2 < frame.shape[1] and y2 < frame.shape[0]:
            
            resized_glasses = cv2.resize(glasses, (glasses_width, glasses_height))
            
            if resized_glasses.shape[2] == 4:
                alpha = resized_glasses[:, :, 3] / 255.0
                for c in range(3):
                    frame[y1:y2, x1:x2, c] = (alpha * resized_glasses[:, :, c] + 
                                            (1 - alpha) * frame[y1:y2, x1:x2, c])
            else:
                frame[y1:y2, x1:x2] = resized_glasses

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    
    faces = face.detectMultiScale(gray, 1.3, 5)
    
    all_eyes = []
    for (x, y, w, h) in faces:
        
        roi_gray = gray[y:y+h//2, x:x+w]
        eyes = eye.detectMultiScale(roi_gray, **eye_params)
        
        
        for (ex, ey, ew, eh) in eyes:
            all_eyes.append((x + ex, y + ey, ew, eh))
    
    apply_glasses(frame, all_eyes)
    
    cv2.imshow('Glasses', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
