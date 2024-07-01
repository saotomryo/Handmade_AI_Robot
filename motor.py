import RPi.GPIO as GPIO

class Motor():
    def __init__(self):
        # Set up pins
        self.MotorPin1   = 17
        self.MotorPin2   = 27
        self.MotorEnable = 22
        self.MotorPin3   = 16
        self.MotorPin4   = 20
        self.MotorEnable2 = 21
        # Set the GPIO modes to BCM Numbering
        GPIO.setmode(GPIO.BCM)
        # Set pins to output
        GPIO.setup(self.MotorPin1, GPIO.OUT)
        GPIO.setup(self.MotorPin2, GPIO.OUT)
        GPIO.setup(self.MotorEnable, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.MotorPin3, GPIO.OUT)
        GPIO.setup(self.MotorPin4, GPIO.OUT)
        GPIO.setup(self.MotorEnable2, GPIO.OUT, initial=GPIO.LOW)

    # Define a motor function to spin the motor
    # direction should be
    # 1(clockwise), 0(stop), -1(counterclockwise)
    def move(self,direction):
        # Clockwise
        if direction == 1:
            # Set direction
            GPIO.output(self.MotorPin1, GPIO.HIGH)
            GPIO.output(self.MotorPin2, GPIO.LOW)
            GPIO.output(self.MotorPin3, GPIO.HIGH)
            GPIO.output(self.MotorPin4, GPIO.LOW)
            # Enable the motor
            GPIO.output(self.MotorEnable, GPIO.HIGH)
            GPIO.output(self.MotorEnable2, GPIO.HIGH)
            print ("Clockwise")
        # Counterclockwise
        if direction == -1:
            # Set direction
            GPIO.output(self.MotorPin1, GPIO.LOW)
            GPIO.output(self.MotorPin2, GPIO.HIGH)
            GPIO.output(self.MotorPin3, GPIO.LOW)
            GPIO.output(self.MotorPin4, GPIO.HIGH)
            # Enable the motor
            GPIO.output(self.MotorEnable, GPIO.HIGH)
            GPIO.output(self.MotorEnable2, GPIO.HIGH)
            print ("Counterclockwise")
        # Stop
        if direction == 0:
            # Disable the motor
            GPIO.output(self.MotorEnable, GPIO.LOW)
            GPIO.output(self.MotorEnable2, GPIO.LOW)
            print ("Stop")

        if direction == 2:
            # Set direction
            GPIO.output(self.MotorPin1, GPIO.HIGH)
            GPIO.output(self.MotorPin2, GPIO.LOW)
            GPIO.output(self.MotorPin3, GPIO.LOW)
            GPIO.output(self.MotorPin4, GPIO.HIGH)
            # Enable the motor
            GPIO.output(self.MotorEnable, GPIO.HIGH)
            GPIO.output(self.MotorEnable2, GPIO.HIGH)
            print ("turn_right")
        if direction == 3:
            # Set direction
            GPIO.output(self.MotorPin1, GPIO.LOW)
            GPIO.output(self.MotorPin2, GPIO.HIGH)
            GPIO.output(self.MotorPin3, GPIO.HIGH)
            GPIO.output(self.MotorPin4, GPIO.LOW)
            # Enable the motor
            GPIO.output(self.MotorEnable, GPIO.HIGH)
            GPIO.output(self.MotorEnable2, GPIO.HIGH)
            print ("turn_left")

    def destroy(self):
        # Stop the motor
        GPIO.output(self.MotorEnable, GPIO.LOW)
        # Release resource
        GPIO.cleanup()

