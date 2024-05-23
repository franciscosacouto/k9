import socket

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print("Server listening on {}:{}".format(SERVER_IP, SERVER_PORT))

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    while True:
        # Receive the predicted label as an integer
        data = client_socket.recv(4)
        if not data:
            break
        predicted_label = int(data.decode().strip())
        print("Predicted label:", predicted_label)

    client_socket.close()
