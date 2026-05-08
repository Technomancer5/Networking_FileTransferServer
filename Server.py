import socket
import os

IP = '0.0.0.0'
PORT = 65432
BUFFER_SIZE = 4096

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print(f"[*] Server ready. Listening on {PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                # 1. Receive the command (first 4 bytes)
                command = conn.recv(4).decode().strip().upper()
                
                # 2. Request Handling Logic [1]
                if command == "PING":
                    conn.sendall(b"PONG")
                    print(f"[*] Ping from {addr}")

                elif command == "LIST":
                    # Remote Access: Send a list of current files [2]
                    files = "\n".join(os.listdir('.'))
                    conn.sendall(files.encode())
                    print(f"[*] Sent file list to {addr}")

                elif command == "PUT":
                    # Basic Upload Logic using 4096-byte chunks [4, 5]
                    filename = "uploaded_file.dat"
                    with open(filename, "wb") as f:
                        while True:
                            data = conn.recv(BUFFER_SIZE)
                            if not data: break
                            f.write(data)
                    print(f"[+] File '{filename}' received from {addr}")

if __name__ == "__main__":
    start_server()