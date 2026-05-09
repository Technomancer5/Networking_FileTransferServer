import socket
import os

IP = '0.0.0.0'
PORT = 65432
BUFFER_SIZE = 4096

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        print(f"[*] Server listening on {PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                command = conn.recv(4).decode().strip().upper()
                
                if command == "PUT":
                    # 1. Receive Folder Name (32 bytes) and Filename (32 bytes)
                    folder = conn.recv(32).decode().strip()
                    filename = conn.recv(32).decode().strip()
                    
                    # 2. Path Normalization: Create folder if it doesn't exist
                    # exist_ok=True prevents errors if the folder is already there
                    os.makedirs(folder, exist_ok=True) 
                    
                    # 3. Join folder and filename safely for Windows/Linux [4]
                    full_path = os.path.join(folder, filename)
                    
                    print(f"[*] Saving to: {full_path}")
                    with open(full_path, "wb") as f:
                        while True:
                            data = conn.recv(BUFFER_SIZE)
                            if not data: break
                            f.write(data)
                    print(f"[+] {filename} saved in {folder}")

if __name__ == "__main__":
    start_server()