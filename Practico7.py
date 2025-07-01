import cv2 
import numpy as np

drawing = False     #true if mouse is pressed
ix, iy = -1, -1

original = cv2.imread("fernet.jpeg", cv2.IMREAD_COLOR)
coca = cv2.imread("coca.jpeg", cv2.IMREAD_COLOR)
cocaTrans = coca.copy()

clone = original.copy()
cropped = original.copy()
buffer =  original.copy()
imgRotada = original.copy()
imgTrasladada = original.copy()
nueva = 0

angle = 0   #Rotación
tx = 0      #Traslación en X
ty = 0      #Traslación en Y
center = None #Rotación
s = 0       #Escala

##### Transformación Afin
aPresionada = 0 # Con esto sabemos si se presionó a para dejar de llamar a la función draw_rectangle
h, w, _ = coca.shape    #Esquinas de la imagen 2 (coca)
dst_points = [(0, 0), (w-1, 0), (0, h-1)]   #puntos de destino
points = []                                 #puntos elegidos por usuario

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, cropped, clone, buffer

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True      
        ix, iy = x, y
        clone = cropped.copy()      #Para actualizar la imagen y que no se superpongan los rectángulos
        
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        clone = cropped.copy()       #Para actualizar la imagen
        cv2.rectangle(clone, (ix, iy), (x, y), (0, 255, 0), 3)      ##cv2.rectangle(img, pto1, pto2, color, grosor, tipo de linea)

        if ix<x and iy<y:        # Para poder hacer el rectángulo de izquierda a derecha o viceversa y de abajo para arriba o viceversa.
            buffer = cropped[iy:y, ix:x]
        elif ix<x and iy>y:
            buffer = cropped[y:iy, ix:x]
        elif ix>x and iy<y:
            buffer = cropped[iy:y, x:ix]
        else:                               #ix>x and iy>y
            buffer = cropped[y:iy, x:ix]
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            clone = cropped.copy()   #Para actualizar la imagen
            cv2.rectangle(clone, (ix, iy), (x, y), (0, 255, 0), 3)

def select_points(event, x, y, flags, param):
    global clone, points, aPresionada, dst_points, cocaTrans

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)

        if len(points) == 3:

            # Realizamos la transformación y obtenemos la matriz correspondiente de transformación.
            M = affine_transform(dst_points, points)

            # le realizamos la transformación a la imagen2 (coca)
            cocaTrans = cv2.warpAffine(coca, M, (clone.shape[1], clone.shape[0]))
            
            # Necesitamos convertir los valores del vector points en tipo np para poder obtener el 4to punto faltante por álgebra.
            pt1 = np.array(points[0])
            pt2 = np.array(points[1])
            pt3 = np.array(points[2])
            
            # Calculamos el 4to punto
            cuartoPto = pt3 + pt2 - pt1
            cuartoPto = tuple(cuartoPto.astype(int))

            mask = np.zeros_like(clone) #mascara negra con poligono blano
            cv2.fillConvexPoly(mask, np.int32([points[0], points[1], cuartoPto, points[2]]), (255, 255, 255))

            mask_inv = cv2.bitwise_not(mask) 
            image1_bg = cv2.bitwise_and(clone, mask_inv) #Conservo todo menos el poligono 
            image2_fg = cv2.bitwise_and(cocaTrans, mask) #incrusto la nueva sobre lo faltante

            #combino
            clone = (cv2.add(image1_bg, image2_fg)).copy() 
            cv2.imshow('image',clone)
            aPresionada = 0
            points.clear()

        else:
            print("Te faltan seleccionar " + str(3- len(points))+ " puntos")

def rotate(image, angle, center = None, scale = 1.0):
    (h,w) = image.shape[:2]

    if center is None:
        center = (w/2, h/2)
    
    M = cv2.getRotationMatrix2D(center, angle, scale)

    rotated = cv2.warpAffine(image, M, (w, h))
    
    return rotated

def translate(image, x, y):
    (h,w) = (image.shape[0], image.shape[1])

    M = np.float32([[1, 0, x],
                    [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (w, h))
    return shifted

def affine_transform(src_points, dst_points):
    global aPresionada
    assert len(src_points) == 3 and len(dst_points) == 3   #Assert checkea que las condiciones que se le pasan sean verdaderas, sino el programa se detiene y tira un AssertionError.
    aPresionada = 0
    return cv2.getAffineTransform(np.float32(src_points), np.float32(dst_points))   #Retornamos la matriz de transformación (2x3)

cv2.namedWindow('image')

print("MENU: \n")
print("- q: Salir\n")
print("- g: Seleccionar rectángulo\n")
print("- r: Restaurar imágen original\n")
print("- s: Rotar, trasladar y escalar\n")
print("- a: Transformación afín\n")

while(1):
    cv2.imshow('image', clone)
    
    if aPresionada:
        cv2.setMouseCallback('image', select_points)  # setMouseCallback permite ejecutar una funcion en la imagen cada vez que lea un evento de mouse.
        
    
    k = cv2.waitKey(1) & 0xFF

    if k == ord('r'):
        cropped = original.copy()
        clone = original.copy()
        aPresionada = 0
        
    elif k == ord('g'):
        cropped = buffer.copy()
        clone = cropped.copy()
        cv2.imwrite("cropped.jpg", buffer)
        
    elif k == ord('q'):
        break

    elif k == ord('s'):
        s = int(input("Escalado: "))
        angle = float(input("Angulo a rotar: "))
        tx = int(input("Traslacion(x): "))
        ty = int(input("Traslacion(y): "))
        
        imgRotada = rotate(buffer, angle, center, s)
        imgTrasladada = translate(imgRotada, tx, ty)

        cropped = imgTrasladada.copy()
        clone = cropped.copy()
        cv2.imwrite("transEuclidea.jpg", imgTrasladada)

    elif k == ord('a'):
        aPresionada = 1
        print("1er punto = esquina superior izquierda\n")
        print("2er punto = esquina superior derecha\n")
        print("3er punto = esquina inferior izquierda\n")
        
cv2.destroyAllWindows() 
 


