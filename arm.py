"""
    See more Arduino code here: https://www.youtube.com/watch?v=md4RQzFbGR0
"""
from setting import *
from utility import *
from servo import *
import math
import time

class Arm():

    def __init__(self, base=0, right=1, left=2, gripper=3):
        self.base = base
        self.right = right
        self.left = left
        self.gripper = gripper
        self.origin()
        say('Arm setup done!')

    def origin(self):
        self.defaultBase = 90
        self.defaultRight = 90
        self.defaultLeft = 90
        self.defaultGripper = 90
        servo.position(self.base, self.defaultBase)
        servo.position(self.right, self.defaultRight)
        servo.position(self.left, self.defaultLeft)
        servo.position(self.gripper, self.defaultGripper)
        say('Here at 0,0,0')
        
    def releases(self):
        servo.release(self.base)
        servo.release(self.right)
        servo.release(self.left)
        servo.release(self.gripper)
        say('Arm released')

    # Servo Base (Theta)
    def moveBase(self, moveToBase, speed=100):
        
        # speed of movement
        sleep = translate(speed,0,100,50,0)
        if speed == 0:
          return
        
        # limit min/max values
        if moveToBase < 0:
            moveToBase = 0
        if moveToBase > 180:
            moveToBase = 180
        
        if moveToBase > self.defaultBase:
            self.defaultBase = moveToBase
            servo.rotate(self.base, 1, sleep, self.defaultBase)
        else:
            self.defaultBase = moveToBase
            servo.rotate(self.base, -1, sleep, self.defaultBase)

    # Servo Gripper
    def moveGripper(self, moveToGripper, speed=100):
        
        # speed of movement
        sleep = translate(speed,0,100,50,0)
        if speed == 0:
          return
        
        # limit min/max values
        if moveToGripper  < 0:
            moveToGripper  = 0
        if moveToGripper  > 90:
            moveToGripper  = 90
        
        if moveToGripper > self.defaultGripper:
            self.defaultGripper = moveToGripper
            servo.rotate(self.gripper, 1, sleep, self.defaultGripper)
        else:
            self.defaultGripper = moveToGripper
            servo.rotate(self.gripper, -1, sleep, self.defaultGripper)

    # Servo Right
    def moveRight(self, moveToRight, speed=100):
        
        # speed of movement
        sleep = translate(speed,0,100,50,0)
        if speed == 0:
          return
        
        servo.release(self.left)
        # limit min/max values
        if moveToRight  < 50:
            moveToRight  = 50
        if moveToRight  > 179:
            moveToRight  = 179
        
        if moveToRight > self.defaultRight:
            self.defaultRight = moveToRight
            servo.rotate(self.right, 1, sleep, self.defaultRight)
        else:
            self.defaultRight = moveToRight
            servo.rotate(self.right, -1, sleep, self.defaultRight)

    # Servo Left
    def moveLeft(self, moveToLeft, speed=100):
      
        # speed of movement
        sleep = translate(speed,0,100,50,0)
        if speed == 0:
          return
        
        servo.release(self.right)
        # limit min/max values
        if moveToLeft  < 5:
            moveToLeft  = 5
        if moveToLeft  > 140:
            moveToLeft  = 140
        
        if moveToLeft > self.defaultLeft:
            self.defaultLeft = moveToLeft
            servo.rotate(self.left, 1, sleep, self.defaultLeft)
        else:
            self.defaultLeft = moveToLeft
            servo.rotate(self.left, -1, sleep, self.defaultLeft)

    # Move the arm along the r axis (polar coordinates), or in height (z)
    def moveKinematic(self, moveToA=90, moveToR=80, moveToZ=80, speed=100):
        
        # limit min/max values
        if (moveToR < 20):
            moveToR = 20
        if (moveToZ < -35):
            moveToZ = -35
        if (moveToR > 130):
            moveToR = 130
        if (moveToZ > 125):
            moveToZ = 125
        
        c = math.sqrt(moveToZ*moveToZ + moveToR*moveToR) # pythagorean theorem
        K = math.atan2(moveToZ, moveToR)
        
        # fixed length bicep and forearm respectively
        a = 81
        b = 81

        B = math.acos((a*a + c*c - b*b) / (2*a*c)) # cosine law
        C = math.pi - 2*B # (180 - A - B) and A==B from isoceles
        C = C * 180 / math.pi # rad --> deg

        rightServoAngle = (K+B) * 180 / math.pi # servo 1 (right)
        X = 90 - rightServoAngle # right angle subtraction
        Y = 90 - X # sum of interior angles again
        W = 180 - C - Y
        leftServoAngle = W
        
        newRightServoAngle = 175-rightServoAngle
        newLeftServoAngle = 90-leftServoAngle

        if (math.isnan(leftServoAngle) != math.isnan(rightServoAngle)):
            print('ERROR: Outside of boundaries!')
            return

        self.moveBase(moveToA, speed)
        #servo.position(self.right, newRightServoAngle) # see REPORT.pdf for explanation
        self.moveRight(newRightServoAngle,speed)
        #servo.position(self.left, newLeftServoAngle) # and diagrams of angle calculations
        self.moveLeft(newLeftServoAngle, speed)
        
arm = Arm()

