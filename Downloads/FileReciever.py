import socket

# Configuration
IP = '0.0.0.0' # Listens on all available network interfaces
PORT = 65432
BUFFER_SIZE = 4096 # Essential for the "Big File" problem [6]

# Create a TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))
    s.listen()
    print(f"Listening on {PORT}...")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        with open("received_file.txt", "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)