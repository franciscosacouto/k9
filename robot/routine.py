import socket
from Buzzer import *
from Control import *
from Servo import *
from time import *
from Ultrasonic import *
from Led import *


# Define server address and port
SERVER_IP = '127.0.0.1'  # localhost
SERVER_PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to server on port", SERVER_PORT)

    # Communication loop
    while True:
        # Receive data from the server
        data = client_socket.recv(1024).decode()

        if not data:
            break

        # Display received message
        print("Server:", data)

except ConnectionResetError:
    print("Connection to server closed unexpectedly.")

finally:
    # Close the connection
    client_socket.close()





control = Control()
sonic = Ultrasonic()
buzzer = Buzzer()
servo = Servo()

# meter as cenas de wifi para conectarem 
led = Led()
led.colorWipe(led.strip, Color(255, 0, 0))
#verificar 
Connection = True
buzzer.run("0")
input= 0
print(Connection)
while True:
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
        


