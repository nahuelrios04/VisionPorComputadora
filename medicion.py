import cv2
import numpy as np

# Variables globales
points = []          # Almacena los 4 puntos de la selección
measure_pts = []     # Para almacenar puntos de medición
img = None           # Imagen original
warped = None        # Imagen rectificada
scale = None         # Factor de escala (píxeles/metro)
real_width = 0.4     # Ancho real del objeto de referencia en metros (AJUSTAR)
real_height = 0.13    # Alto real del objeto de referencia en metros (AJUSTAR)

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
    # p_origen [A,B,C,D]
    p_origen = np.float32(p_origen)

    # Diferencia de puntos BA, DC, CA y DB

def mouse_selection(event, x, y, flags, param):
    """Callback para selección de puntos iniciales"""
    global points
    
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        
        if len(points) > 1:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 2)
        
        cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)

def mouse_measure(event, x, y, flags, param):
    """Callback para medición de distancias"""
    global measure_pts, warped, scale
    
    if event == cv2.EVENT_LBUTTONDOWN:
        measure_pts.append((x, y))
        cv2.circle(warped, (x, y), 5, (0, 0, 255), -1)
        
        if len(measure_pts) == 2:
            # Calcula distancia en metros
            dx_px = measure_pts[1][0] - measure_pts[0][0]
            dy_px = measure_pts[1][1] - measure_pts[0][1]
            
            dx_m = dx_px / scale
            dy_m = dy_px / scale
            distance = np.sqrt(dx_m**2 + dy_m**2)
            
            # Dibuja línea y muestra distancia en metros
            cv2.line(warped, measure_pts[0], measure_pts[1], (0, 255, 255), 2)
            mid_x = (measure_pts[0][0] + measure_pts[1][0]) // 2
            mid_y = (measure_pts[0][1] + measure_pts[1][1]) // 2
            cv2.putText(warped, f"{distance:.2f} metros", (mid_x, mid_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow("Imagen Rectificada", warped)
            print(f"Distancia medida: {distance:.2f} metros")
            measure_pts = []

def rectificar_imagen():
    """Realiza la rectificación perspectiva"""
    global img, points, warped, scale
    
    # Ordena puntos
    ordered_points = ordenaPuntos(points)
    
    # Define rectángulo destino (conservando relación de aspecto)
    aspect_ratio = real_width / real_height
    rect_width = 800
    rect_height = int(rect_width / aspect_ratio)
    
    dst_pts = np.array([
        [0, rect_height - 1],
        [0, 0],
        [rect_width - 1, 0],
        [rect_width - 1, rect_height - 1]
    ], dtype="float32")
    
    # Calcula homografía
    src_pts = np.array(ordered_points, dtype="float32")
    H = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img, H, (rect_width, rect_height))
    
    # Calcula escala (píxeles por metro)
    scale = rect_width / real_width
    
    return warped, scale

def main():
    global img, points, warped, scale
    
    # Cargar imagen
    img_path = "patente.png"  # Cambiar por tu imagen
    img = cv2.imread(img_path)
    
    if img is None:
        print("Error: No se pudo cargar la imagen")
        return
    
    # Paso 1: Selección de puntos
    cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)
    cv2.setMouseCallback("Seleccionar 4 puntos (A, B, C, D)", mouse_selection)
    
    print("Selecciona los 4 vértices del objeto de referencia (en cualquier orden)")
    print("Presiona cualquier tecla cuando hayas terminado")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    if len(points) != 4:
        print("Error: Debes seleccionar exactamente 4 puntos")
        return
    
    # Paso 2: Rectificación
    warped, scale = rectificar_imagen()
    print(f"Escala calculada: {scale:.2f} píxeles/metro | {1/scale:.6f} metros/píxel")
    # Paso 3: Medición
    cv2.imshow("Imagen Rectificada", warped)
    cv2.setMouseCallback("Imagen Rectificada", mouse_measure)
    
    print("\nInstrucciones:")
    print("- Haz clic en dos puntos para medir la distancia en metros")
    print("- Presiona 'r' para reiniciar mediciones")
    print("- Presiona 'ESC' para salir")
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):  # Reiniciar
            warped, _ = rectificar_imagen()
            cv2.imshow("Imagen Rectificada", warped)
            measure_pts = []
        elif key == 27:  # ESC para salir
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
