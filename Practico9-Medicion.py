import cv2
import numpy as np

# ====== Variables Globales ======
points = []          # Almacena los 4 puntos seleccionados
measure_pts = []     # Almacena los 2 puntos para medir
img = None           # Imagen original
warped = None        # Imagen rectificada
scale = None         # Escala (píxeles/metro)

# ====== Función para ordenar puntos (A, B, C, D) en sentido horario ======
def ordenaPuntos(points):
    # Calcula los módulos de las distancias al origen
    mod = []
    for x, y in points:
        mod.append(np.sqrt(x**2 + y**2))
    
    new_points = [0, 0, 0, 0]
    
    # A: Punto más cercano al origen (módulo mínimo)
    new_points[0] = points.pop(mod.index(min(mod)))
    
    # D: Punto más lejano al origen (módulo máximo)
    new_points[3] = points.pop(mod.index(max(mod)))
    
    # Ordena B y C según coordenada Y (B tiene Y menor)
    if points[0][1] < points[1][1]:
        new_points[1] = points[0]
        new_points[2] = points[1]
    else:
        new_points[1] = points[1]
        new_points[2] = points[0]
    
    return new_points

# ====== Callback para seleccionar 4 puntos con el ratón ======
def mouse_callback(event, x, y, flags, param):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        if len(points) > 1:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 2)
        cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)
        if len(points) == 4:
            cv2.destroyWindow("Seleccionar 4 puntos (A, B, C, D)")

# ====== Callback para medir distancias en la imagen rectificada ======
def measure_distance(event, x, y, flags, param):
    global measure_pts, warped, scale
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
            cv2.putText(warped, f"{distance:.2f}m", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.imshow("Imagen Rectificada (Medición)", warped)
            print(f"Distancia medida: {distance:.2f} metros")
            measure_pts = []  # Reinicia para nueva medición

# ====== Rectificación de perspectiva ======
def rectify_perspective(img_path, real_width, real_height):
    global img, points, warped, scale
    
    # Carga la imagen y permite seleccionar 4 puntos
    img = cv2.imread(img_path)
    cv2.imshow("Seleccionar 4 puntos (A, B, C, D)", img)
    cv2.setMouseCallback("Seleccionar 4 puntos (A, B, C, D)", mouse_callback)
    cv2.waitKey(0)
    
    # Ordena los puntos en sentido horario (A, B, C, D)
    points = ordenaPuntos(points)
    
    # Define el rectángulo de destino (misma relación de aspecto)
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
    # Configuración (ajustar según la imagen)
    img_path = "patente.png"  # Cambiar por tu imagen
    real_width = 2.0          # Ancho real del objeto de referencia (metros)
    real_height = 1.0         # Alto real del objeto de referencia (metros)
    
    # Rectifica la perspectiva
    warped, scale = rectify_perspective(img_path, real_width, real_height)
    cv2.imshow("Imagen Rectificada (Medición)", warped)
    cv2.setMouseCallback("Imagen Rectificada (Medición)", measure_distance)
    
    print(f"Escala calculada: {scale:.2f} píxeles/metro")
    print("Instrucciones:")
    print("- Haz clic en dos puntos para medir la distancia.")
    print("- Presiona 'r' para reiniciar las mediciones.")
    print("- Presiona 'ESC' para salir.")
    
    # Bucle principal
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):  # Reinicia la imagen rectificada
            points = []
            measure_pts = []
            warped, scale = rectify_perspective(img_path, real_width, real_height)
            cv2.imshow("Imagen Rectificada (Medición)", warped)
        elif key == 27:  # Sale con ESC
            break
    
    cv2.destroyAllWindows()
