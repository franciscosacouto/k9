import socket
import time 

head = 0
up = 0
tilt = 0
legs = 0

def start_server():
    # Define server address and port
    SERVER_IP = '0.0.0.0'  # Listen on all interfaces
    SERVER_PORT = 8000

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on port {SERVER_PORT}")

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        while True:
            # Receive message from client
            data = client_socket.recv(1024).decode()
            if not data:
                print("Client disconnected")
                break
            print("Received:", data)
            #execute_action(data)     
            
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        client_socket.close()
        server_socket.close()
        print("Server shutdown")

def execute_action(input_data):
    global head
    global up
    global tilt
    global legs
    led.colorWipe(led.strip,Color(255,0,0))

    if input_data == '0':
        for i in range(0,180):
            servo.setServoAngle(2,i/3)
            servo.setServoAngle(3,i*2/3)

            servo.setServoAngle(5,i/3)
            servo.setServoAngle(6,i/2)

            servo.setServoAngle(9,i*2/3)
            servo.setServoAngle(10,i*2/3)

            servo.setServoAngle(12,i*2/3)
            servo.setServoAngle(13,i/3)
            time.sleep(0.03)

        led.colorWipe(led.strip,Color(0,255,0))


        tilt = 0
        legs = 0
        up = 0

    elif input_data == '1': 
        if up == 0:#bem
            for i in range(0,180):
                servo.setServoAngle(2,i*2/3)
                servo.setServoAngle(3,i)

                servo.setServoAngle(5,i*2/3)
                servo.setServoAngle(6,i*5/6)

                servo.setServoAngle(9,i/2)
                servo.setServoAngle(10,i/3)

                servo.setServoAngle(12,i)
                servo.setServoAngle(13,i*2/3)
                time.sleep(0.03)

            up=1
        else:
            for i in range(0,180):
                servo.setServoAngle(2,i/3)
                servo.setServoAngle(3,i*2/3)

                servo.setServoAngle(5,i/3)
                servo.setServoAngle(6,i/2)

                servo.setServoAngle(9,i*2/3)
                servo.setServoAngle(10,i*2/3)

                servo.setServoAngle(12,i*2/3)
                servo.setServoAngle(13,i/3)
                time.sleep(0.03)
            
            up = 0    
        led.colorWipe(led.strip,Color(0,255,0))
    
    
    elif input_data == '2':
        if head == 0:
            for i in range(0,120): 
                servo.setServoAngle(15,i)
                time.sleep(0.03)
            head=1
        else:
            for i in range(-120,0): 
                servo.setServoAngle(15,-i)
                time.sleep(0.03)
            head = 0    
        led.colorWipe(led.strip,Color(0,255,0))

    elif input_data == '3':
        if legs == 0:
            for i in range(0,180):
                servo.setServoAngle(2,i*2/3)
                servo.setServoAngle(3,i)

                servo.setServoAngle(5,i/3)
                servo.setServoAngle(6,i/2)

                servo.setServoAngle(9,i*2/3)
                servo.setServoAngle(10,i*2/3)

                servo.setServoAngle(12,i)
                servo.setServoAngle(13,i*2/3)
                time.sleep(0.03)
            
            legs=1
        else:
            for i in range(0,180):
                servo.setServoAngle(2,i/3)
                servo.setServoAngle(3,i*2/3)

                servo.setServoAngle(5,i/3)
                servo.setServoAngle(6,i/2)

                servo.setServoAngle(9,i*2/3)
                servo.setServoAngle(10,i*2/3)

                servo.setServoAngle(12,i*2/3)
                servo.setServoAngle(13,i/3)
                time.sleep(0.03)
            
            legs = 0    
        led.colorWipe(led.strip,Color(0,255,0))

    elif input_data == '4':
            if tilt == 0:
                for i in range(0,180):
                    servo.setServoAngle(2,i*2/3)
                    servo.setServoAngle(3,i)

                    servo.setServoAngle(5,i*2/3)
                    servo.setServoAngle(6,i*5/6)

                    servo.setServoAngle(9,i*2/3)
                    servo.setServoAngle(10,i*2/3)

                    servo.setServoAngle(12,i*2/3)
                    servo.setServoAngle(13,i/3)
                    time.sleep(0.03)
                
                tilt=1
            else:
                for i in range(0,180):
                    servo.setServoAngle(2,i/3)
                    servo.setServoAngle(3,i*2/3)

                    servo.setServoAngle(5,i/3)
                    servo.setServoAngle(6,i/2)

                    servo.setServoAngle(9,i*2/3)
                    servo.setServoAngle(10,i*2/3)

                    servo.setServoAngle(12,i*2/3)
                    servo.setServoAngle(13,i/3)
                    time.sleep(0.03)
                
                tilt = 0    
            led.colorWipe(led.strip,Color(0,255,0))



start_server()