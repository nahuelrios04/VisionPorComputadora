import cv2 
import numpy as np 
from Detector_Objetos import * 
diccionario = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parametros = cv2.aruco.DetectorParameters_create()

detector = DetectorFondo()

cap = cv2.VideoCapture(0) 
cap.set(3,640) 
cap.set(4,480)

while True: 
    ret, frame = cap.read() 
    if ret == False: break 

    esquinas, _, _ =cv2.aruco.detectMarkers(frame, diccionario, parameters = parametros ) 
    esquinas_ent = np.int0(esquinas)
    cv2.polylines(frame, esquinas_ent, True, (0,0,255), 5)

    perimetro_aruco = cv2.arcLength(esquinas_ent[0], True)

    proporcion_cm = perimetro_aruco / 16 

    contornos = detector.deteccion_objetos(frame)
    for cont in contornos: 
        rectangulo = cv2.minAreaRect(cont) 
        (x,y),(an,al), angulo = rectangulo 
        ancho = an / proporcion_cm 
        alto = al / proporcion_cm 
        cv2.circle(frame,(int(x), int(y)),5, (255,255,0),-1)
        rect = cv2.boxPoints(rectangulo) 
        rect = np. np.int0(rect)

        cv2.polyLines(frames, [rect], True, (0,255,0),2)

        cv2.putText(frame,"Ancho: {} cm".format(round(ancho,1)), (int(x),int(y-15)), cv2.LINE_AA, 0.8, (150,0,255,2))
        cv2.putText(frame,"Largo: {} cm".format(round(alto,1)), (int(x),int(y+15)), cv2.LINE_AA, 0.8, (75,0,75,2))

    cv2.imshow('Medicion de objetos', frame)

    t = cv2.waitKey(1) 
    if t==27: 
        break 
    cv2.destroyAllWindows()

