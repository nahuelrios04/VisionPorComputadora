import cv2 

class DetectorFondo(): 
    def __init__(self):
        pass
    def deteccion_objetos(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,19,5)
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
        objetos_contornos = [] 
        for cnt in contornos: 
            area = cv2.contourArea(cnt) 
            if area > 2000: 
                objetos_contornos.append(cnt)
        return objetos_contornos 
