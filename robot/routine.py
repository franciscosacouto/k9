import socket
import time 
import Control
import Servo
import Ultrasonic 
import Buzzer

control = Control()
sonic = Ultrasonic()
buzzer = Buzzer()
servo = Servo()

# meter as cenas de wifi para conectarem 

#verificar 
Connection = True
buzzer.run("0")
input= 0
print(Connection)
while Connection:
    buzzer.run("1")
    time.sleep(1)
    buzzer.run("0")
    if input == 0:
        servo.setServoAngle(10,0)
        servo.setServoAngle(5,0)
        servo.setServoAngle(2,180)
        servo.setServoAngle(13,180)
    if input == 1:
        servo.setServoAngle(10,180)
        servo.setServoAngle(5,180)
        servo.setServoAngle(2,0)
        servo.setServoAngle(13,0)
    if input == 2:
        servo.setServoAngle(15,180)
        

    if input == 3:
        control.upAndDown("2")
    else:
        time.sleep(1)
        


