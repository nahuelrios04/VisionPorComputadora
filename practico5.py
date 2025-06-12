import cv2
import numpy as n
import math as m

drawing = False
ix, iy = -1, -1
rx, ry = -1, -1

img = cv2.imread('pepsi.png')  
img_original = img.copy()

def euclidean_transform(img_section, angle_deg, tx, ty): #traslada y rota
    angle_rad = m.radians(angle_deg) #transformo el angulo en radianes porque le pedi al usuario en deg
    cos_a = m.cos(angle_rad)
    sin_a = m.sin(angle_rad)
 

    h, w = img_section.shape[:2] #shape = (alto, ancho, canales) me devuelve una tupla pero con el :2 solo los dos primeros alto y ancho

    # Calcular posición centrada inicial
    start_x = (4*w - w) // 2 + tx
    start_y = (4*h - h) // 2 + ty

    # Matriz de transformación
    M = n.array([
        [cos_a, sin_a, start_x],
        [-sin_a, cos_a, start_y]
    ], dtype=n.float32)
    
    transformed = cv2.warpAffine(img_section, M, (4*w, 4*h)) #Aplico LA MTRIZ M A LA SECCION - EL TAMAÑP DE SALIDA ES 4 VECES MAS GRANDE PARA ASEGURAR QUE NADA QUEDE AFUERA Esto asegura que nada quede recortado si la rotación desplaza partes fuera del área original.

    return transformed


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, rx, ry, drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = img_original.copy()
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rx, ry = x, y
        cv2.rectangle(img, (ix, iy), (rx, ry), (0, 255, 0), 2)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)
###############################################################################LOOP ##############################33
while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(20) & 0xFF

    if k == ord('r'):
        img = img_original.copy()
        ix, iy, rx, ry = -1, -1, -1, -1
        print("Imagen restaurada.")

    elif k == ord('q') or k == 27:  # 'q' o ESC
        print("Saliendo del programa...")
        break
    elif k == ord('e'): #aca activo la transformada
        if ix != -1 and iy != -1 and rx != -1 and ry != -1:
            x1, y1 = min(ix, rx), min(iy, ry)
            x2, y2 = max(ix, rx), max(iy, ry)
            roi = img_original[y1:y2, x1:x2] 
            #ROI ES LA IMAGEN RECORTADA RECORTED ORIGINAL IMAGE #################



############### LE PIDO AL USUARIO LOS DATOS #######################

            angle = float(input("Ángulo de rotación (grados): "))
            tx = float(input("Traslación en X: "))
            ty = float(input("Traslación en Y: "))

######################################### LLAMO A LA FUNCION DE TRANSFORMADA ECLUDIANA DECLARADA AL INICIO ####################################33

            transformed_roi = euclidean_transform(roi, angle, tx, ty) #llamo a la funcion
            cv2.imwrite("transformada.jpg", transformed_roi)
            print("Imagen transformada guardada como 'transformada.jpg'")
            

cv2.destroyAllWindows()
