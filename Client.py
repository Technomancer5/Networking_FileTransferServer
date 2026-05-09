import socket
import os

SERVER_IP = '192.168.1.171'
PORT = 65432
BUFFER_SIZE = 4096

def run_ping():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.sendall(b"PING")
        return s.recv(BUFFER_SIZE).decode()

def get_remote_list(folder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.sendall(b"LIST")
        # Send folder header so server knows where to look
        s.sendall(f"{folder:<32}".encode())
        return s.recv(BUFFER_SIZE).decode()

def upload_file(filename, remote_folder):
    if not os.path.exists(filename):
        print(f"[!] Error: Local file {filename} not found.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.sendall(b"PUT ") 
        s.sendall(f"{remote_folder:<32}".encode())
        s.sendall(f"{filename:<32}".encode())
        
        with open(filename, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                s.sendall(chunk)
    print(f"[+] Finished uploading {filename} to {remote_folder}")

if __name__ == "__main__":
    # 1. Ask for destination folder
    dest_folder = input("Step 1: Enter the remote destination folder: ")

    # 2. Ping to verify connection
    print(f"Step 2: Pinging server... ", end="")
    status = run_ping()
    print(f"Server Response: {status}")

    # 3. List files from that specific folder
    print(f"\nStep 3: Files already in '{dest_folder}':")
    print(get_remote_list(dest_folder))

    # 4. Ask which file(s) to upload
    print("\nStep 4: Upload Selection")
    user_input = input("Enter local filename(s) to upload (space separated): ")
    
    for file in user_input.split():
        upload_file(file, dest_folder)