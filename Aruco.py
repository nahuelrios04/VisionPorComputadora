import cv2 
import numpy as np 
from Detector_Objetos import * 

# Configuración inicial
diccionario = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parametros = cv2.aruco.DetectorParameters_create()
detector = DetectorFondo()

# Configuración de cámara
cap = cv2.VideoCapture(0) 
cap.set(3, 640) 
cap.set(4, 480)

while True: 
    ret, frame = cap.read() 
    if not ret: 
        print("Error al capturar el frame")
        break 

    # 1. Detección de marcadores ArUco
    esquinas, ids, _ = cv2.aruco.detectMarkers(frame, diccionario, parameters=parametros)
    
    proporcion_cm = None  # Inicializamos la variable

    if len(esquinas) > 0:
        # Dibujar los marcadores detectados
        cv2.aruco.drawDetectedMarkers(frame, esquinas, ids)
        
        # Calcular proporción solo si hay marcadores
        esquinas_ent = np.int0(esquinas)
        perimetro_aruco = cv2.arcLength(esquinas[0], True)
        proporcion_cm = perimetro_aruco / 16 
        
        # Dibujar contorno del marcador
        cv2.polylines(frame, [esquinas_ent[0]], True, (0,0,255), 2)
    else:
        cv2.putText(frame, "No se detecto marcador ArUco", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 2. Detección y medición de objetos (solo si tenemos proporción)
    if proporcion_cm is not None:
        contornos = detector.deteccion_objetos(frame)
        
        for cont in contornos: 
            # Solo procesar contornos significativos
            if cv2.contourArea(cont) < 500:  # Filtro por área mínima
                continue
                
            rectangulo = cv2.minAreaRect(cont) 
            (x, y), (an, al), angulo = rectangulo 
            
            # Calcular dimensiones en cm
            ancho = an / proporcion_cm 
            alto = al / proporcion_cm 
            
            # Dibujar resultados
            cv2.circle(frame, (int(x), int(y)), 5, (255, 255, 0), -1)
            rect = cv2.boxPoints(rectangulo) 
            rect = np.int0(rect)
            cv2.polylines(frame, [rect], True, (0, 255, 0), 2)
            
            # Mostrar medidas
            cv2.putText(frame, f"Ancho: {round(ancho, 1)} cm", 
                       (int(x), int(y-15)), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (150, 0, 255), 2)
            cv2.putText(frame, f"Largo: {round(alto, 1)} cm", 
                       (int(x), int(y+15)), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (75, 0, 75), 2)

    # Mostrar frame
    cv2.imshow('Medicion de objetos', frame)

    # Salir con ESC
    if cv2.waitKey(1) == 27: 
        break 

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
