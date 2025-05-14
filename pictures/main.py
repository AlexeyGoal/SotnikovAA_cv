import cv2

def detect_stars(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.equalizeHist(gray)
    
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    stars_count = 0
    min_area = 100    
    
    for cnt in contours:
        
        if cv2.contourArea(cnt) < min_area:
            continue
            
        
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        
        if len(approx) == 10 and cv2.contourArea(cnt) > 100:
            hull = cv2.convexHull(approx, returnPoints=False)
            
            if hull is not None and len(hull) > 0:
                defects = cv2.convexityDefects(approx, hull)
                if defects is not None and len(defects) > 3:
                    stars_count += 1

            
    return stars_count



cap = cv2.VideoCapture("output.avi")

count_img = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    filtered_contours = [cnt for cnt in contours]
    
    if len(filtered_contours) == 1 and detect_stars(frame) == 1:
         
        count_img += 1
    
cap.release()
print(count_img)
