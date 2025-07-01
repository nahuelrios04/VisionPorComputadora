import cv2
import numpy as n
import math as m

drawing = False
ix, iy = -1, -1
rx, ry = -1, -1

img = cv2.imread('pepsi.png')  
img_original = img.copy()

print("Seleccione una porcion de la imagen con el mouse..")
print("Seleccione r para restaurar en caso de no estar conforme con su seleccion.")
print("Seleccione q para salir del programa.")
print("Seleccione s para aplicar transformada + escala.")
def euclidean_transform(img_section):
    # Obtener parámetros del usuario
    angle_deg = float(input("Ángulo de rotación (grados): "))
    tx = float(input("Traslación en X (píxeles): "))
    ty = float(input("Traslación en Y (píxeles): "))
    scale = float(input("Factor de escala: "))
    
    # Convertir ángulo a radianes
    angle_rad = n.radians(angle_deg)
    cos_a = n.cos(angle_rad)
    sin_a = n.sin(angle_rad)
    
    # Dimensiones originales
    h, w = img_section.shape[:2]
    
    # Calcular nuevas dimensiones después de rotación y escala
    new_w = int((w * abs(cos_a) + h * abs(sin_a))*scale)
    new_h = int((w * abs(sin_a) + h * abs(cos_a))*scale)

    # Matriz de transformación compuesta (rotación + escala + traslación)
    # 1. Matriz de rotación y escala
    rotation_matrix = n.array([
        [scale * cos_a, scale * sin_a, 0],
        [-scale * sin_a, scale * cos_a, 0]
    ])
    
    # 2. Ajustar para centrar la imagen
    # Calculamos cómo se mueve el centro con la rotación
    center_x = w / 2
    center_y = h / 2
    new_center_x = (rotation_matrix[0,0] * center_x + rotation_matrix[0,1] * center_y)
    new_center_y = (rotation_matrix[1,0] * center_x + rotation_matrix[1,1] * center_y)
    
    # 3. Añadir traslación para centrar + traslación del usuario
    rotation_matrix[0,2] = (new_w / 2) - new_center_x + tx
    rotation_matrix[1,2] = (new_h / 2) - new_center_y + ty
    
    # Aplicar transformación
    transformed = cv2.warpAffine(
        img_section, 
        rotation_matrix, 
        (new_w, new_h),  # Tamaño de salida calculado
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)  ) 
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
    k = cv2.waitKey(1) 
    if k == ord('r'):
        img = img_original.copy()
        ix, iy, rx, ry = -1, -1, -1, -1
        print("Imagen restaurada.")

    elif k == ord('q'): 
        print("Saliendo del programa...")
        break
    elif k == ord('s'): #aca activo la transformada
        if ix != -1 and iy != -1 and rx != -1 and ry != -1:
            x1, y1 = min(ix, rx), min(iy, ry)
            x2, y2 = max(ix, rx), max(iy, ry)
            roi = img_original[y1:y2, x1:x2] 
            #ROI ES LA IMAGEN RECORTADA RECORTED ORIGINAL IMAGE #################
   

############### LE PIDO AL USUARIO LOS DATOS #######################


######################################### LLAMO A LA FUNCION DE TRANSFORMADA ECLUDIANA DECLARADA AL INICIO ####################################33

            transformed_roi = euclidean_transform(roi) #llamo a la funcion
            cv2.imwrite("transformada.jpg", transformed_roi)
            img = transformed_roi
            print("Imagen transformada guardada como 'transformada.jpg'")

cv2.destroyAllWindows()
