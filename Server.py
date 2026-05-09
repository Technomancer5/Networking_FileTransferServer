import socket
import os

IP = '0.0.0.0'
PORT = 65432
BUFFER_SIZE = 4096 # Essential for "Big File" stability [5]

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print(f"[*] Server listening on {PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                command = conn.recv(4).decode().strip().upper()
                
                if command == "PING":
                    conn.sendall(b"PONG")
                    print(f"[*] Ping verified for {addr}")

                elif command == "LIST":
                    # Receive which folder to look in (32 bytes)
                    folder = conn.recv(32).decode().strip()
                    if os.path.exists(folder) and os.path.isdir(folder):
                        files = "\n".join(os.listdir(folder))
                        conn.sendall(files.encode() if files else b"(Folder is empty)")
                    else:
                        # Auto-create the folder if it's new [3, 6]
                        os.makedirs(folder, exist_ok=True)
                        conn.sendall(b"(New folder created, currently empty)")
                    print(f"[*] Sent list for folder: '{folder}' to {addr}")

                elif command == "PUT":
                    folder = conn.recv(32).decode().strip()
                    filename = conn.recv(32).decode().strip()
                    os.makedirs(folder, exist_ok=True)
                    
                    full_path = os.path.join(folder, filename) # Cross-platform safety [3, 7]
                    with open(full_path, "wb") as f:
                        while True:
                            data = conn.recv(BUFFER_SIZE)
                            if not data: break
                            f.write(data)
                    print(f"[+] {filename} successfully saved in {folder}")

if __name__ == "__main__":
    start_server()