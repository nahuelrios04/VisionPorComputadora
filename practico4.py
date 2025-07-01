import cv2
import numpy as np

drawing = False  # Verdadero si el mouse está presionado
ix, iy = -1, -1  #posicion nula porque 0 es una posicion de la imagen 
fx, fy = -1, -1
img = cv2.imread('pepsi.png')  # img va a ser la modificable 
img_original = (cv2.imread('pepsi.png')).copy()  #replica una imagen totalmente independiente asi guardamos la version original 

print("Seleccione una porcion de la imagen con el mouse..")
print("Seleccione r para restaurar en caso de no estar conforme con su seleccion.")
print("Seleccione g para guardar la seleccion.")
print("Seleccione q para salir del programa.")


################################### FUNCION DIBUJAR ####################################################################33

def draw(event, x, y, flags, param): #esta funcion solo para eventos del mouse y tomar sus posiciones
    global ix, iy, drawing, mode, img, fx, fy

    if event == cv2.EVENT_LBUTTONDOWN: #chequea si se presiona click izquierdo 
        drawing = True #bandera de modo dibujo 
        ix, iy = x, y #setea inicio de seleccion 

    elif event == cv2.EVENT_MOUSEMOVE: #si se mueve el mouse 
        if drawing:
            img = img_original.copy() #para que no solaplen los rectangulos 
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 255), 3) #color y ancho

    elif event == cv2.EVENT_LBUTTONUP: #si suelto el click izquierdo
        drawing = False
        fx, fy = x, y #setea final de seleccion 
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

#######################################NUESTRO MAIN ##########################################################################

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF   #espera que el usr presione una tecla espera un 1ms sino sigue el codigo, 0xff se queda con los ultimos 8 bits para asegurar compatibilidad con wds u otros que devuelven longitudes mas largas, sino hay nada devuelve -1
    if k == ord('g'):
        if ix != -1 and iy != -1 and fx != -1 and fy != -1:
            x1, y1 = min(ix, fx), min(iy, fy)   #la funcion minimo 
            x2, y2 = max(ix, fx), max(iy, fy)   #funcion maximo 
            cropped = img_original[y1:y2, x1:x2] #de la imagen original define alto y ancho 
            cv2.imwrite('Recorte.jpg', cropped)
            print("La imagen ha sido guardada correctamente como 'Recorte.jpg'")
    elif k == ord('r'):
        img = img_original.copy()
        ix, iy, fx, fy = -1, -1, -1, -1
        print("Imagen restaurada para una nueva selección")
    elif k == ord('q'):
        break

cv2.destroyAllWindows()
