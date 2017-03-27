import sys
import cv2
import urllib
import numpy as np
from datetime import datetime
import argparse
import logging

def run(rpi_name, rpi_ip):
    absolute_link = '/home/cuda/workspace/experiment_data/videos/'
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    d =  datetime.now()
    file_name = d.strftime("%m-%d-%y_%H")
    file_name = absolute_link + rpi_name + '_' + file_name +'.avi'
    print file_name
    hour = eval(d.strftime("%H"))
    print hour
    out = cv2.VideoWriter(str(file_name),fourcc, 17, (640,480))

    stream=urllib.urlopen('http://' + rpi_ip + ':8080/stream/video.mjpeg')
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
                frame = cv2.flip(frame,0)
                cv2.imshow('i',frame)
                out.write(frame)
                current_hour = eval(datetime.now().strftime("%H"))

                if hour != current_hour:
                    print current_hour
                    hour = current_hour
                    out.release()
                    file_name = datetime.now().strftime("%m-%d-%y_%H")
                    file_name = absolute_link + rpi_name + '_' + file_name + '.avi'
                    out = cv2.VideoWriter(file_name,fourcc,17, (640,480))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print 'breaking'
                    break
        except Exception as ex:
            logging.exception("An error occured")
    # Release everything if job is finished
    print 'releasing...'
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', help="RPI IP address", type=str, default='172.26.55.186')
    parser.add_argument('-n', '--name', help="RPI NAME", type=str, default="rpi1")
    args = parser.parse_args()

    rpi_name = args.name
    rpi_ip = args.ip
    run(rpi_name, rpi_ip)
