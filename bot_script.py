from picamera.array import PiRGBArray
import RPi.GPIO as GPIO 

import time
import picamera
import cv2


#Setting up DC motors on RaspBerry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup([23,24,27,22,5,6],GPIO.OUT)
GPIO.setwarnings(False)
p10 = GPIO.PWM(22,50)
p11 = GPIO.PWM(27,50)
p12 = GPIO.PWM(5,50)
p13 = GPIO.PWM(6,50)

def main():
    #Starting from a known distance
    KNOWN_DISTANCE = 30.0
    KNOWN_WIDTH = 2.76
    LEFT_CAMERA_SENSOR = 295
    RIGHT_CAMERA_SENSOR = 345
    
    #Setting to arbitrary large value
    Current_distance = 100000000.00
    centered = False
    moving = False
    
    ref = cv2.imread("Face2_189x302.jpg")
    
    #Setting up the picamera
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    capture = PiRGBArray(camera, size = (640, 480))
    time.sleep(0.1)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    #Sets up the face detector
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Find face from reference image
    ref_g = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(ref_g, 1.1, 4)

    # Calculate focal length of camera using equation
    focalLength = faces[0][2] * KNOWN_DISTANCE / KNOWN_WIDTH
    # 
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
            
            #Determines if the Raspberry Pi should be moving left, right or center based on the position of the image in the camera feed
            if x < LEFT_CAMERA_SENSOR and moving == False:
                Move("Left")
                moving = True
            if x > RIGHT_CAMERA_SENSOR and moving == False:
                Move("Right")
                moving = True
               
            #If the image is centered on the camera, have the Raspberry Pi move forward
            if(x >= LEFT_CAMERA_SENSOR and x <= RIGHT_CAMERA_SENSOR):
                centered = True
                if(moving == True):
                    moving = False
            #If the image is closed enough (Current_distance <= 32, then the Raspberry Pi is close enough to the picture to pick it up)
            if centered == True and Current_distance > 32.0:
                move("Forward")
                moving = True
            else:
                moving = False
                move("Stop")
            
            GPIO.cleanup()
            # Puts text on the camera frame indicating the estimated distance from the object
            cv2.putText(frame, str(getDist(KNOWN_WIDTH, focalLength, w)) + " in", (20, 40), font, 1, (0, 255, 255), 2, cv2.LINE_4)

        # To show the camera frame onto the screen
        cv2.imshow('frame', frame)

        # Trunctes the feed (Now that the program is out of the loop)
        capture.truncate(0);

        # Automatically stops the Raspberry Pi if q is pressed
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    GPIO.cleanup()
    cv2.destroyAllWindows()

# Calculates estimated distance using the equation from before
def getDist(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

# Directs the DC motors to move
def move(direction):
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
