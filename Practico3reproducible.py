import cv2
import sys
import subprocess
import os

def convert_to_vlc_compatible(input_path):
    # Configuración de entrada
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error al abrir el video de entrada")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) , int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    delay = int(1000/fps) if fps >0 else 33 
    # Archivo temporal de trabajo
    temp_file = 'temp_output.avi'
    final_file = 'MarioSalida.mp4'

    out = cv2.VideoWriter(temp_file, fourcc,fps, (width, height),isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir a gris y luego a BGR (3 canales)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        out.write(gray_bgr)
        cv2.imshow('Muestra del video en grises', gray_bgr) 
        if cv2.waitKey(delay) == ord('q'): 
            break
        

    cap.release()
    out.release()

    # Conversión final con FFmpeg para máxima compatibilidad
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', temp_file,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            final_file
        ], check=True)
        print(f"Video convertido con éxito: {final_file}")
        return True
    except Exception as e:
        print(f"Error en conversión FFmpeg: {e}")
        return False
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <video_entrada>")
        sys.exit(1)
    
    if convert_to_vlc_compatible(sys.argv[1]):
        print("Proceso completado exitosamente")
    else:
        print("Error en el proceso de conversión")
