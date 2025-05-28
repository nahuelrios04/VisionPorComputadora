import cv2
import numpy as np

drawing = False  # Verdadero si el mouse está presionado
mode = True      # Verdadero para rectángulo, alternar con 'm'
ix, iy = -1, -1
rx, ry = -1, -1
img = cv2.imread('pepsi.png')  # Carga tu imagen aquí
img_original = img.copy()

print("Seleccione una porcion de la imagen con el mouse..")
print("Seleccione r para restaurar en caso de no estar conforme con su seleccion.")
print("Seleccione g para guardar la seleccion.")
print("Seleccione q para salir del programa.")

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, rx, ry

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = img_original.copy()
            if mode:
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rx, ry = x, y
        if mode:
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        else:
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('g'):
        if ix != -1 and iy != -1 and rx != -1 and ry != -1:
            x1, y1 = min(ix, rx), min(iy, ry)
            x2, y2 = max(ix, rx), max(iy, ry)
            cropped = img_original[y1:y2, x1:x2]
            cv2.imwrite('Recorte.jpg', cropped)
            print("La imagen ha sido guardada correctamente como 'Recorte.jpg'")
    elif k == ord('r'):
        img = img_original.copy()
        ix, iy, rx, ry = -1, -1, -1, -1
        print("Imagen restaurada para una nueva selección")
    elif k == ord('q'):
        break

cv2.destroyAllWindows()
