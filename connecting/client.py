import socket

# Define server parameters
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432      # Port to listen on

# Create and configure socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind((HOST, PORT))
client_socket.listen(1)
print(f"Client waiting for server to connect on {HOST}:{PORT}")

# Accept a connection
conn, addr = client_socket.accept()
print(f"Connected by {addr}")

# Receive the message from the server
data = conn.recv(1024)  # Buffer size
message = data.decode('utf-8')
print(f"Message received from server: {message}")

# Send acknowledgment back to the server
ack_message = "Acknowledged: Message received"
conn.sendall(ack_message.encode('utf-8'))
print(f"Acknowledgment sent to server: {ack_message}")

# Close the connection
conn.close()
client_socket.close()

