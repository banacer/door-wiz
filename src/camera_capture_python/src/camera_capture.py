import cv2
dif

cap = cv2.VideoCapture(0)
# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
d =  datetime.now()
file_name = d.strftime("%m-%d-%y_%H")
file_name = file_name+'.avi'
print file_name
hour = eval(d.strftime("%H"))
print hour
out = cv2.VideoWriter(str(file_name),fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        current_hour = eval(datetime.now().strftime("%H"))
        
        if hour != current_hour:
            print current_hour
            out.release()
            file_name = d.strftime("%m-%d-%y_%H")
            file_name = file_name+'.avi'
            out = cv2.VideoWriter(file_name,fourcc, 20.0, (640,480))
        
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
