import cv2
import numpy as n
import math as m

drawing = False
ix, iy = -1, -1
rx, ry = -1, -1

img = cv2.imread('pepsi.png')  
img_original = img.copy()

def euclidean_transform(img_section, angle_deg, tx, ty):
    angle_rad = m.radians(angle_deg)
    cos_a = m.cos(angle_rad)
    sin_a = m.sin(angle_rad)

    # Matriz de transformación (2x3)
    M = n.array([
        [cos_a, sin_a, tx],
        [-sin_a, cos_a, ty]
    ], dtype=n.float32)

    h, w = img_section.shape[:2]
    cx, cy = w / 2, h / 2
    new_cx, new_cy = 2 * w, 2 * hransformed = cv2.warpAffine(img_section, M, (4*w, 4*h))
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

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('r'):
        img = img_original.copy()
        ix, iy, rx, ry = -1, -1, -1, -1
        print("Imagen restaurada.")

    elif k == ord('e'):
        if ix != -1 and iy != -1 and rx != -1 and ry != -1:
            x1, y1 = min(ix, rx), min(iy, ry)
            x2, y2 = max(ix, rx), max(iy, ry)
            roi = img_original[y1:y2, x1:x2]

            angle = float(input("Ángulo de rotación (grados): "))
            tx = float(input("Traslación en X: "))
            ty = float(input("Traslación en Y: "))

            transformed_roi = euclidean_transform(roi, angle, tx, ty)
            cv2.imwrite("transformada.jpg", transformed_roi)
            print("Imagen transformada guardada como 'transformada.jpg'")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()
