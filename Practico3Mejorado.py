import cv2 as o
import sys 

if len(sys.argv) > 1:
    ArchName = sys.argv[1]
else:
    print("Pass a filename as first argument...")
    sys.exit(0)

# Inicializar captura de video
video = o.VideoCapture(ArchName)

# Obtener FPS del video y calcular delay
fps = video.get(o.CAP_PROP_FPS)
delay = int(1000 / fps) if fps > 0 else 33  # Si FPS = 0, usar 30 FPS por defecto

# Configurar VideoWriter con el mismo FPS
fourcc = o.VideoWriter_fourcc('X', 'V', 'I', 'D')
framesize = (int(video.get(o.CAP_PROP_FRAME_WIDTH)), int(video.get(o.CAP_PROP_FRAME_HEIGHT)))
VideoOut = o.VideoWriter('Output.avi', fourcc, fps, framesize)

while video.isOpened():
    ret, frame = video.read()
    
    if ret:
        gray = o.cvtColor(frame, o.COLOR_BGR2GRAY)
        VideoOut.write(gray)
        o.imshow('Video en grises', gray)
        
        # Usar delay calculado del FPS
        if o.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        break

video.release()
VideoOut.release()
o.destroyAllWindows()
