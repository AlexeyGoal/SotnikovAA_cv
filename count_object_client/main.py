import cv2 
import zmq 
import numpy as np 

address = "84.237.21.36"

port = 6002 

contex = zmq.Context()
socket = contex.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE,b"")
socket.connect(f"tcp://{address}:{port}")

def detect_shape(c):
    perimeter= cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
    
    if len(approx) == 4:  
        return "cube"
    else:  
        (x,y), radius = cv2.minEnclosingCircle(c)
        area = cv2.contourArea(c)
        circle_area = np.pi * (radius ** 2)
        
        if abs(1 - (area / circle_area)) < 0.2:  
            return "ball"


while True:
    message = socket.recv()
    frame = cv2.imdecode(np.frombuffer(message,np.uint8),-1)
    
    key = chr(cv2.waitKey(1) & 0xFF)
    if key =="q":
        break 
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blurr = cv2.GaussianBlur(hsv, (9, 9), 0)
 
    _, thresh = cv2.threshold(blurr[:,:,2], 150, 255, cv2.THRESH_BINARY)
    
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_ERODE,np.ones((5, 5), np.uint8), iterations=6)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE,np.ones((5, 5), np.uint8), iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cubes = 0 
    balls = 0 

    for i in contours:
        area = area = cv2.contourArea(i)
        if area < 150:
            continue
        if detect_shape(i) == "cube":
            cubes += 1
        if detect_shape(i) == "balls":
            balls += 1 

        
        

    cv2.putText(frame,f"Count {len(contours)}",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
    cv2.putText(frame,f"cubes {cubes}",(10,80),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
    cv2.putText(frame,f"balls {balls}",(10,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
    
                   

    
    cv2.imshow("Clients",frame)





