import socket
import sys

# Define server address and port
SERVER_IP = '127.0.0.1'  # localhost
SERVER_PORT = 8000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening on", SERVER_IP, "port", SERVER_PORT)

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Connected to client:", client_address)

# Communication loop
try:
    while True:
        # Get keyboard input
        message = input("Type a message to send to client: ")

        # Send message to the client
        client_socket.send(message.encode())

        if message.lower() == 'exit':
            break

finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
