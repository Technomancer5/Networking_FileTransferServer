import socket

# Configuration
DEST_IP = '192.168.x.x' # Replace with the Receiver's IP address
PORT = 65432
FILE_TO_SEND = "my_document.txt"

# Create a TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((DEST_IP, PORT)) # The "Handshake" [5]
    with open(FILE_TO_SEND, "rb") as f:
        # Stream the file in chunks to avoid memory crashes [6]
        chunk = f.read(4096)
        while chunk:
            s.sendall(chunk)
            chunk = f.read(4096)