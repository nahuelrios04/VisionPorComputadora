import cv2
import numpy as np

# ====== Variables Globales ======
points = []          # Almacena los 4 puntos seleccionados
measure_pts = []     # Almacena los 2 puntos para medir
img = None           # Imagen original
warped = None        # Imagen rectificada
scale = None         # Escala (píxeles/metro)
selecting = True     # Controla el estado de selección

# ====== Función para ordenar puntos (A, B, C, D) en sentido horario ======
def ordenaPuntos(puntos):
    # Calcula el centroide
    centro = np.mean(puntos, axis=0)
    
    # Ordena los puntos según el ángulo con respecto al centro
    puntos_ordenados = sorted(puntos, key=lambda p: np.arctan2(p[1]-centro[1], p[0]-centro[0]))
    
    # Asegurar orden horario: A (sup-izq), B (sup-der), C (inf-der), D (inf-izq)
    return [puntos_ordenados[0], puntos_ordenados[1], puntos_ordenados[3], puntos_ordenados[2]]

# ====== Callback para seleccionar 4 puntos con el ratón ======
def mouse_callback(event, x, y, flags, param):
    global points, img, selecting
    
    if event == cv2.EVENT_LBUTTONDOWN and selecting:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        
        if len(points) > 1:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 2)
        
        cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)
        
        if len(points) == 4:
            selecting = False
            cv2.destroyWindow("Seleccionar 4 puntos (A, B, C, D)")

# ====== Callback para medir distancias en la imagen rectificada ======
def measure_callback(event, x, y, flags, param):
    global measure_pts, warped
    
    if event == cv2.EVENT_LBUTTONDOWN:
        measure_pts.append((x, y))
        cv2.circle(warped, (x, y), 5, (0, 0, 255), -1)
        
        if len(measure_pts) == 2:
            # Calcula la distancia en píxeles y la convierte a metros
            dx = (measure_pts[1][0] - measure_pts[0][0]) / scale
            dy = (measure_pts[1][1] - measure_pts[0][1]) / scale
            distance = np.sqrt(dx**2 + dy**2)
            
            # Dibuja la línea y muestra la distancia
            cv2.line(warped, measure_pts[0], measure_pts[1], (0, 255, 255), 2)
            mid_x = (measure_pts[0][0] + measure_pts[1][0]) // 2
            mid_y = (measure_pts[0][1] + measure_pts[1][1]) // 2
            cv2.putText(warped, f"{distance:.2f}m", (mid_x, mid_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow("Imagen Rectificada (Medición)", warped)
            print(f"Distancia medida: {distance:.2f} metros")
            measure_pts = []

# ====== Rectificación de perspectiva ======
def rectify_perspective():
    global img, points, warped, scale
    
    # Ordena los puntos en sentido horario
    points = ordenaPuntos(points)
    
    # Define el rectángulo de destino (misma relación de aspecto)
    real_width = 2.0  # Ancho real en metros (ajustar)
    real_height = 1.0 # Alto real en metros (ajustar)
    
    aspect_ratio = real_width / real_height
    rect_width = 800  # Ancho arbitrario para la imagen rectificada
    rect_height = int(rect_width / aspect_ratio)
    
    dst_pts = np.array([
        [0, rect_height - 1],          # A (esquina inferior izquierda)
        [0, 0],                        # B (esquina superior izquierda)
        [rect_width - 1, 0],           # C (esquina superior derecha)
        [rect_width - 1, rect_height - 1]  # D (esquina inferior derecha)
    ], dtype="float32")
    
    # Calcula la homografía y aplica la transformación
    src_pts = np.array(points, dtype="float32")
    H = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img, H, (rect_width, rect_height))
    
    # Calcula la escala (píxeles/metro)
    scale = rect_width / real_width
    
    return warped, scale

# ====== Programa Principal ======
if __name__ == "__main__":
    # Carga la imagen
    img_path = "patente.png"  # Cambiar por tu imagen
    img = cv2.imread(img_path)
    
    if img is None:
        print("Error: No se pudo cargar la imagen")
        exit()
    
    # Paso 1: Selección de puntos
    cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)
    cv2.setMouseCallback("Seleccionar 4 puntos (A, B, C, D)", mouse_callback)
    
    # Espera a que se seleccionen los 4 puntos
    while selecting:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Salir con ESC
            cv2.destroyAllWindows()
            exit()
    
    # Paso 2: Rectificación
    warped, scale = rectify_perspective()
    
    # Paso 3: Medición
    cv2.imshow("Imagen Rectificada (Medición)", warped)
    cv2.setMouseCallback("Imagen Rectificada (Medición)", measure_callback)
    
    print(f"Escala calculada: {scale:.2f} píxeles/metro")
    print("Instrucciones:")
    print("- Haz clic en dos puntos para medir la distancia.")
    print("- Presiona 'r' para reiniciar las mediciones.")
    print("- Presiona 'ESC' para salir.")
    
    # Bucle principal
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):  # Reinicia las mediciones
            warped, _ = rectify_perspective()
            cv2.imshow("Imagen Rectificada (Medición)", warped)
            measure_pts = []
        elif key == 27:  # Sale con ESC
            break
    
    cv2.destroyAllWindows()
