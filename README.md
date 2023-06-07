# Photo-Frame-Collector
Built using a Raspberry Pi and programmed through Python, the robot identifies a picture frame with a specified image that has a face from up to 3m away, moves towards the image, picks it up and and returns the photo to the original starting position of the robot. Used DC motors for robot movement and servo motors to control arm movement, including moving the arms up and down to retrieve the photo. 

## Libraries and Dependencies used (PyPI pacakge manager):
- OpenCV: Open source library that uses machine vision. Installation: `pip install opencv-python-headless`.
- GPIO: Library used to control GPIO (the computer board) and various DC, servo motors on the Raspberry Pi. Installation: `pip install RPi.GPIO`.
