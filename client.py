import socket

# Define server address and port
SERVER_IP = '192.168.2.3'
SERVER_PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to server on port", SERVER_PORT)

    # Communication loop
    while True:
        # Send message to the server
        message = input("Enter a message to send to server: ")
        client_socket.send(message.encode())

        
except ConnectionResetError:
    print("Connection to server closed unexpectedly.")

finally:
    # Close the connection
    client_socket.close()
