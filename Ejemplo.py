import cv2 

img = cv2.imread('homero.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Imagen.jpg') 

while(true) 
    ret, img = cap.read() 
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    cv2.inshow('img')


