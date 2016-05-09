import sys
import cv2
import urllib
import numpy as np
from datetime import datetime

#get params
rpi_name =  str(sys.argv[1])
rpi_ip = str(sys.argv[2])

fourcc = cv2.cv.CV_FOURCC(*'XVID')
d =  datetime.now()
file_name = d.strftime("%m-%d-%y_%H")
file_name = rpi_name + '_' + file_name +'.avi'
print file_name
hour = eval(d.strftime("%H"))
print hour
out = cv2.VideoWriter(str(file_name),fourcc, 7.0, (640,480))

stream=urllib.urlopen('http://' + rpi_ip + ':9090/video_feed')
bytes=''
while True:
    try:
        bytes+=stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
            #cv2.imshow('i',frame)
            current_hour = eval(datetime.now().strftime("%H"))

            if hour != current_hour:
                print current_hour
                hour = current_hour
                out.release()
                file_name = datetime.now().strftime("%m-%d-%y_%H")
                file_name = rpi_name + '_' + file_name + '.avi'
                out = cv2.VideoWriter(file_name,fourcc, 7.0, (640,480))
            #print type(frame)
            #width = np.size(frame, 1) #here is why you need numpy!  (remember to "import numpy as np")
            #height = np.size(frame, 0)
            #print 'width:', width,' height: ', height
            out.write(frame)
            #cv2.imshow('frame',frame)
            #cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as ex:
        print 'exception is: ', str(ex)
# Release everything if job is finished
print 'releasing...'
out.release()
cv2.destroyAllWindows()