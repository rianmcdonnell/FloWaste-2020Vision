import numpy as np
import cv2
import pyrealsense2 as rs
import matplotlib.pyplot as plt

#config = rs.config()
#config.enable_record_to_file('test.bag')
pipe = rs.pipeline()
profile = pipe.start()
#profile = pipe.start(config)

try:
    while True:
        frames = pipe.wait_for_frames()
        
        color_frames = frames.get_color_frame()
        depth_frames = frames.get_depth_frame()
        color = np.asanyarray(color_frames.get_data())
        color = cv2.cvtColor(color,cv2.COLOR_RGB2BGR)

        img = cv2.cvtColor(color,cv2.COLOR_RGB2GRAY)
        img = cv2.medianBlur(img,5)

        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1.2,640,
                            param1=50,param2=50,minRadius=125,maxRadius=175)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))

            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(color,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(color,(i[0],i[1]),2,(0,0,255),3)

        cv2.imshow('Circles',color)

        #depth = np.asanyarray(depth_frames.get_data())
        #cv2.imshow('depth',depth)
        
        #color2 = cv2.cv2Color(color,cv2.COLOR_RGB2BGR)
        #cv2.imshow('frame',color2)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipe.stop()
    cv2.destroyAllWindows()