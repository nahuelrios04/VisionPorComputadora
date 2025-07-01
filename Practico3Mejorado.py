import cv2 as o
import sys 
if len(sys.argv) > 1:
    ArchName = sys.argv[1]
else:
    print("Pase el archivo como primer argumento...")
    sys.exit(0)
video = o.VideoCapture(ArchName)
fps = video.get(o.CAP_PROP_FPS)
fourcc = o.VideoWriter_fourcc(*'MJPG')  # Alternativas: 'MJPG', 'H264', 'X264'
framesize = (int(video.get(o.CAP_PROP_FRAME_WIDTH)), int(video.get(o.CAP_PROP_FRAME_HEIGHT))) #alto y ancho de los fotogramas 
# Especificar isColor=False para video en escala de grises
delay = int(1000 / fps) if fps > 0 else 33  #calcula en ms, entre frames el tiempo de espera


VideoOut = o.VideoWriter('Output.mp4', fourcc, fps, framesize) 


while video.isOpened():
    ret, frame = video.read() #ret es true si leyo el frame correctamente 
    if ret:
        gray = o.cvtColor(frame, o.COLOR_BGR2GRAY)
        VideoOut.write(gray) #guardamos el frame procesado y pasado a gris en el archivo de salida
        o.imshow('Video en grises', gray)
        if o.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        break
video.release()
VideoOut.release()
o.destroyAllWindows()
