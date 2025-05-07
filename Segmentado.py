import cv2 as o 
img = o.imread("pepsi.png",0)
h,w = img.shape #se toman las dimensiones de la imagen en ese orden
limite = 128 
for i in range(h): #se realizan dos recorridos como una matriz en fin y cabo una imagen es una matriz de 1 y 0s.
    for j in range(w): 
        if img[i,j] > limite:
            img[i,j] = 255 #Transforma el pixel en blanco 
        else:
            img[i,j] = 0 #transforma el pixel en negro 

o.imwrite("umbralizado.png", img) 
print("El proceso de umbralizado ha sido realizado correctamente")
