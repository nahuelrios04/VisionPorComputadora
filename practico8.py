import cv2
import numpy as np
import sys


def getPoints(event, x, y, flags, param):
    global points, img, img_aux
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append([x, y])
        else:
            points.clear()
            points.append([x, y])
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.circle(img, (x, y), 5, (120, 255, ), -1)
        print(f"Punto seleccionado en cordenadas: ({x},{y})")

def ordenaPuntos(points):

    #A ------ B
    #|        |
    #C ------ D

    mod = [] 
    for x, y in points:
        mod.append(np.sqrt(x**2 + y**2)) #calcula los modulos de las distancias 

    new_points = [0, 0, 0, 0]

    new_points[0] = points.pop(mod.index(min(mod))) #define A
    new_points[3] = points.pop(mod.index(max(mod)) - 1) #define D -1 porque pop borra 

    if points[0][1] < points[1][1]: #compara Y
        new_points[1] = points[0] #define C y B 
        new_points[2] = points[1]
    else:
        new_points[1] = points[1]
        new_points[2] = points[0]

    return new_points


def rectificar(img, p_origen):
    p_origen = np.float32(p_origen)

    difBA = p_origen[1] - p_origen[0]
    difDC = p_origen[3] - p_origen[2]
    difCA = p_origen[2] - p_origen[0]
    difDB = p_origen[3] - p_origen[1]
    wAB = np.sqrt(difBA[0]**2 + difBA[1]**2)
    wCD = np.sqrt(difDC[0]**2 + difDC[1]**2)
    hAC = np.sqrt(difCA[0]**2 + difCA[1]**2)
    hBD = np.sqrt(difDB[0]**2 + difDB[1]**2)

    # Ancho y largo maximos
    W = max(int(wAB), int(wCD)) - 1
    H = max(int(hBD), int(hAC)) - 1

    # Puntos destino
    p_destino = np.float32([[0, 0], [W, 0], [0, H], [W, H]])
    M = cv2.getPerspectiveTransform(p_origen, p_destino)
    img_salida = cv2.warpPerspective(img, M, (W, H))
    return img_salida

if(len(sys.argv) > 1):
    filename = sys.argv[1]  # guarda el nombre del archivo
else:
    print("Pass a filename as first argument")
    sys.exit(0)  # sale del programa

img = cv2.imread(filename, cv2.IMREAD_COLOR)
img_aux = np.copy(img)


draw = False
points = []

cv2.namedWindow('imagen')
cv2.setMouseCallback('imagen', getPoints)

print("Con el mouse puede seleccione 4 puntos donde rectificar")
print("Con la letra \'h\'se rectificará la imagen con los puntos seleccionados")
print("Con la letra \'r\' se reinicia la seleccion de puntos")
print("Con la letra \'q\' finaliza la ejecución del programa")

while True:
    cv2.imshow('imagen', img)
    # cv2.imwrite('prueba.jpg', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('r'):
        img = cv2.imread(filename)
        points = []
    if key == ord('h'):
        if len(points) < 4:
            print("\nDebe seleccionar 4 puntos primero")
        else:
            img = img_aux.copy()
            points = ordenaPuntos(points)
            img = rectificar(img, points)
            cv2.imwrite('output.jpg', img)

cv2.destroyAllWindows()
