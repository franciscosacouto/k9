import socket

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
