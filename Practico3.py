import cv2 as o 
import sys 

if(len(sys.argv)>1): #cuando en la terminal escribimos python bla bla1 mi bla1 es el argumento 1 
    ArchName= sys.argv[1]
else:
    print("Pass a filename as first argument...")
    sys.exit(0)

video=o.VideoCapture(ArchName) 
fourcc = o.VideoWriter_fourcc('X','V','I','D') 
framesize=(640,480)
VideoOut=o.VideoWriter('Output.avi', fourcc, 20.0, framesize) 

delay = 33 
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:
        gray = o.cvtColor(frame, o.COLOR_BGR2GRAY)
        out.write(gray)
        o.imshow('Image gray', gray)
        if o.waitKey(delay) &OxFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()
o.destroyAllWindows()

