import socket
import os

IP, PORT, BUFFER_SIZE = '0.0.0.0', 65432, 4096

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
                    folder = conn.recv(32).decode().strip()
                    filename = conn.recv(32).decode().strip()
                    os.makedirs(folder, exist_ok=True)
                    full_path = os.path.join(folder, filename)

                    # --- Overwrite Check ---
                    if os.path.exists(full_path):
                        conn.sendall(b"EXISTS")
                        response = conn.recv(7).decode().strip().upper() # "PROCEED" or "CANCEL"
                        if response != "PROCEED":
                            print(f"[!] Transfer aborted for {filename}")
                            continue
                    else:
                        conn.sendall(b"READY ")

                    # --- Chunked Data Reception ---
                    with open(full_path, "wb") as f:
                        while True:
                            data = conn.recv(BUFFER_SIZE)
                            if not data: break
                            f.write(data)
                    print(f"[+] Successfully saved {filename} to {folder}")

if __name__ == "__main__":
    start_server()