import cv2
import numpy as np

# Variables globales
points = []          # Almacena los 4 puntos de la selección
measure_pts = []     # Para almacenar puntos de medición
img = None           # Imagen original
warped = None        # Imagen rectificada
scale = None         # Factor de escala (píxeles/metro)

def ordenaPuntos(points):
    pts = np.array(points, dtype="float32")
    
    # Ordenar por coordenada x (izquierda a derecha)
    x_sorted = pts[np.argsort(pts[:, 0]), :]
    
    left_pts = x_sorted[:2]
    right_pts = x_sorted[2:]
    
    left_pts = left_pts[np.argsort(left_pts[:, 1])]
    A = left_pts[0]  # Superior izquierdo
    D = left_pts[1]  # Inferior derecho 
    
    right_pts = right_pts[np.argsort(right_pts[:, 1])]
    B = right_pts[0]  # Superior derecho
    C = right_pts[1]  # Inferior izquierdo
    
    return [A, B, C, D]

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
    global measure_pts, warped, scale
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(measure_pts) < 2:
            measure_pts.append((x, y))
            cv2.circle(warped, (x, y), 5, (0, 0, 255), -1)
            
            if len(measure_pts) == 2:
                dx_px = measure_pts[1][0] - measure_pts[0][0]
                dy_px = measure_pts[1][1] - measure_pts[0][1]
                
                dx_m = dx_px / scale
                dy_m = dy_px / scale
                distance = np.sqrt(dx_m**2 + dy_m**2)
                
                # Dibuja línea y muestra distancia en metros
                cv2.line(warped, measure_pts[0], measure_pts[1], (0, 255, 255), 2)
                mid_x = (measure_pts[0][0] + measure_pts[1][0]) // 2
                mid_y = (measure_pts[0][1] + measure_pts[1][1]) // 2
                cv2.putText(warped, f"{distance:.5f} m", (mid_x, mid_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                cv2.imshow("Imagen Rectificada", warped)
                print(f"Distancia medida: {distance:.5f} metros")
        else:
            # Reiniciar medición si ya hay 2 puntos
            measure_pts = [(x, y)]
            warped = rectificar_imagen()[0]
            cv2.circle(warped, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("Imagen Rectificada", warped)

def rectificar_imagen():
    global img, points, warped, scale, real_width, real_height

    if len(points) != 4:
        print("Error: Se necesitan exactamente 4 puntos")
        return None, None

    # Ordena puntos
    ordered_points = ordenaPuntos(points)
    width_px = np.linalg.norm(np.array(ordered_points[1]) - np.array(ordered_points[0]))
    
    # Calcula la escala (píxeles por metro)
    scale = width_px / real_width
    
    # Define el tamaño de la imagen rectificada basado en la escala y dimensiones reales
    rect_width = int(real_width * scale)  # Ancho calculado automáticamente
    rect_height = int(real_height * scale)  # Alto calculado automáticamente
    dst_pts = np.array([
        [0, 0],                         # A (sup-izq)
        [rect_width - 1, 0],             # B (sup-der)
        [rect_width - 1, rect_height - 1],  # C (inf-der)
        [0, rect_height - 1]             # D (inf-izq)
    ], dtype="float32")
    # Asegurar que los puntos origen están en el mismo orden que los destino
    src_pts = np.array(ordered_points, dtype="float32")
    
    # Calcula homografía
    H = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img, H, (rect_width, rect_height))
    
    # Calcula escala (píxeles por metro)
    scale = rect_width / real_width
    
    return warped, scale

def main():
    global img, points, warped, scale, real_width, real_height
    
    img_path = "jtag.png"  # Cambiar por tu imagen
    img = cv2.imread(img_path)
    
    real_width = float(input('Ingrese el ancho del objeto conocido en metros: '))      # Ancho real del objeto de referencia en metros (AJUSTAR)
    real_height = float(input('Ingrese el alto del objeto conocido en metros: '))    # Alto real del objeto de referencia en metros (AJUSTAR)
    if img is None:
        print("Error: No se pudo cargar la imagen")
        return
    
    cv2.namedWindow("Seleccionar 4 puntos (A, B, C, D)", cv2.WINDOW_NORMAL)
    cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)
    cv2.setMouseCallback("Seleccionar 4 puntos (A, B, C, D)", mouse_selection)
    
    print("Selecciona los 4 vértices del objeto de referencia (en cualquier orden)")
    print("Presiona cualquier tecla cuando hayas terminado")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    if len(points) != 4:
        print("Error: Debes seleccionar exactamente 4 puntos")
        return
    
    warped, scale = rectificar_imagen()
    if warped is None:
        return
    
    print(f"Escala calculada: {scale:.2f} píxeles/metro | {1/scale:.6f} metros/píxel")
    
    # Paso 3: Medición
    cv2.namedWindow("Imagen Rectificada", cv2.WINDOW_NORMAL)
    cv2.imshow("Imagen Rectificada", warped)
    cv2.setMouseCallback("Imagen Rectificada", mouse_measure)
    
    print("\nInstrucciones:")
    print("- Haz clic en dos puntos para medir la distancia en metros")
    print("- Haz clic nuevamente para comenzar una nueva medición")
    print("- Presiona 'ESC' para salir")
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC para salir
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
