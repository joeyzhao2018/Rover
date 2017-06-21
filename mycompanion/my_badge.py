import json
import time
import sys
import cv2
import zbar
from PIL import Image
import subprocess as sub
import numpy as np

class Badge(object):
    def __init__(self):
        self.resolution = (640, 480)

    def read_badge(self):
        # Initialise USB camera
        print("Initializing USB camera...")
        frame_capture = cv2.VideoCapture(0)

        # allow camera to warm up
        time.sleep(0.5)

        # Initialise OpenCV window
        #if FULLSCREEN:
        #    cv2.namedWindow("#badgeView", cv2.WND_PROP_FULLSCREEN)
        #    cv2.setWindowProperty("#badgeView", cv2.WND_PROP_FULLSCREEN, 1)
        #else:
        #    cv2.namedWindow("#badgeView")
        #print("Setting window properties")
        #cv2.namedWindow("#badgeView", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("#badgeView", cv2.WND_PROP_FULLSCREEN, 1)

        print("Starting zbar")
        scanner = zbar.Scanner()

        now = time.time()

        # Capture frames from the camera
        while time.time() - now < 20:
            # Capture frame-by-frame
            ret, frame = frame_capture.read()

            # raw detection code
            print("captured frame")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
            pil = Image.fromarray(gray)
            width, height = pil.size
            raw = pil.tostring()

            # create a reader
            image = scanner.scan(gray)
            sid = 0
            # extract results
            for symbol in image:
                frame_capture.release()
                cv2.destroyAllWindows()

                # do something useful with results
                sid = symbol.data.decode('ascii')
                #pil.save('badge.png')
                print('decoded', symbol.type, 'symbol', '"%s"' % sid)
                return sid
            # Display the resulting frame
            #cv2.imshow('#badgeView', frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #   return 0

        frame_capture.release()
        cv2.destroyAllWindows()
        return -1 

if __name__ == '__main__':
    b = Badge()
    print("SID: {}".format(b.read_badge()))
