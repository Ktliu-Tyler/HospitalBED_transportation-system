import RPi.GPIO as GPIO
from time import sleep
import multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor:
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B,
                 motor_mode='BCM', setWarn: bool=False):

        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        mode = getattr(GPIO, motor_mode)
        GPIO.setmode(mode)
        GPIO.setwarnings(setWarn)
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmA.start(0)
        self.pwmB.start(0)
        self.mySpeed = 0

    def move(self, speed=0.5, turn=0., t=0.):
        speed *= 100
        turn *= 70
        leftSpeed = speed - turn
        rightSpeed = speed + turn

        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100
        # print(leftSpeed,rightSpeed)
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        if leftSpeed > 0:
            GPIO.output(self.In1A, GPIO.HIGH);GPIO.output(self.In2A, GPIO.LOW)
        else:
            GPIO.output(self.In1A, GPIO.LOW);GPIO.output(self.In2A, GPIO.HIGH)
        if rightSpeed > 0:
            GPIO.output(self.In1B, GPIO.HIGH);GPIO.output(self.In2B, GPIO.LOW)
        else:
            GPIO.output(self.In1B, GPIO.LOW);GPIO.output(self.In2B, GPIO.HIGH)
        sleep(t)

    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        self.mySpeed = 0
        sleep(t)

class Mecanum:
    def __init__(self, M1A, M1B, M2A, M2B, M3A, M3B, M4A, M4B,
                 motor_mode='BOARD', set_warn: bool = False):
        self.MA = []
        self.MB = []
        self.MA.append(M1A)
        self.MA.append(M2A)
        self.MA.append(M3A)
        self.MA.append(M4A)
        self.MB.append(M1B)
        self.MB.append(M2B)
        self.MB.append(M3B)
        self.MB.append(M4B)
        mode = getattr(GPIO, motor_mode)
        GPIO.setmode(mode)
        GPIO.setwarnings(set_warn)
        for i in range(4):
            GPIO.setup(self.MA[i], GPIO.OUT)
            self.MA[i] = GPIO.PWM(self.MA[i], 100)
            self.MA[i].start(0)
            GPIO.setup(self.MB[i], GPIO.OUT)
            self.MB[i] = GPIO.PWM(self.MB[i], 100)
            self.MB[i].start(0)

    def turn(self, direction):
        if direction == 1:
            pass
        elif direction == 2:
            pass
        elif direction == 3:
            pass
        elif direction == 4:
            pass



def main():
    motor.move(0.5, 0, 2)
    motor.stop(2)
    motor.move(-0.5, 0, 2)
    motor.stop(2)
    motor.move(0, 0.5, 2)
    motor.stop(2)
    motor.move(0, -0.5, 2)
    motor.stop(2)


if __name__ == '__main__':
    motor = Motor(33, 35, 37, 32, 36, 38, 'BOARD', False)
    main()
