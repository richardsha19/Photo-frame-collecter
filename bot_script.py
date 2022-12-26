from picamera.array import PiRGBArray
import RPi.GPIO as GPIO 

import time
import picamera
import cv2



GPIO.setmode(GPIO.BCM)
GPIO.setup([23,24,27,22,5,6],GPIO.OUT)
GPIO.setwarnings(False)
p10 = GPIO.PWM(22,50)
p11 = GPIO.PWM(27,50)
p12 = GPIO.PWM(5,50)
p13 = GPIO.PWM(6,50)

def main():
    KNOWN_DISTANCE = 30.0
    KNOWN_WIDTH = 2.76
    Current_distance = 100000000.00
    centered = False
    moving = False
    
    ref = cv2.imread("/home/pi/Desktop/Face2_189x302.jpg")
    
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    capture = PiRGBArray(camera, size = (640, 480))
    time.sleep(0.1)
    
    font = cv2.FONT_HERSHEY_SIMPLEX

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Find face from reference image
    ref_g = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(ref_g, 1.1, 4)

    # Calculate focal length of camera using equation
    focalLength = faces[0][2] * KNOWN_DISTANCE / KNOWN_WIDTH
    # Same as before
    for f in camera.capture_continuous(capture, format = "bgr", use_video_port = True):
        frame = f.array
        cv2.imshow('frame', frame)

        # Same as before
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Same as before
        faces = face_detector.detectMultiScale(gray, 1.1, 4)

        # Same as before
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            
            Current_distance = getDist(KNOWN_WIDTH, focalLength, w)
            
            if x < 295 and moving == False:
                print("Left")
            if x > 345 and moving == False:
                print("Right")
                
            
            if(x > 295 and x < 345):
                centered = True
                if(moving == True):
                    moving = False
                
            if centered == True and Current_distance > 32.0:
                move("Forward")
                moving = True
            else:
                print("Stop")
                moving = False
                move("Stop")
            
            GPIO.cleanup()
                        # Puts text on the image indicating the estimated distance from the object
            cv2.putText(frame, str(getDist(KNOWN_WIDTH, focalLength, w)) + " in", (20, 40), font, 1, (0, 255, 255), 2, cv2.LINE_4)

        # Same as before
        cv2.imshow('frame', frame)

        # Same as before
        capture.truncate(0);

        # Same as before
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    GPIO.cleanup()
        # Same as before
    cv2.destroyAllWindows()

# Calculates estimated distance using the equation from before
def getDist(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

def move(direction):
    #while(direction != "Stop"):
    if(direction == "Forward"):
        print("Forward")
        GPIO.output(27,GPIO.HIGH)
        GPIO.output(5,GPIO.HIGH)
        p10.start(30)
        p13.start(30)
    if(direction == "Backward"):
        print("Backward")
        GPIO.output(22,GPIO.HIGH)
        GPIO.output(6,GPIO.HIGH)
        p11.start(30)
        p12.start(30)
    if(direction == "Right"):
        print("Right")
        GPIO.output(22,GPIO.HIGH)
        GPIO.output(5,GPIO.HIGH)
        p10.start(30)
        p12.start(30)
    if(direction == "Left"):
        print("Left")
        GPIO.output(27,GPIO.HIGH)
        GPIO.output(6,GPIO.HIGH)
        p11.start(30)
        p13.start(30)
        

    if(direction == "Stop"):
        print("STOP")
        p10.stop()
        p11.stop()
        p12.stop()
        p13.stop()
        GPIO.cleanup()
    GPIO.cleanup()
        
if __name__ == "__main__":
    main()
