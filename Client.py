import socket
import os

SERVER_IP = '192.168.1.171'
PORT = 65432
BUFFER_SIZE = 4096

def upload_file(filename, remote_folder):
    if not os.path.exists(filename):
        print(f"[!] Local file {filename} not found.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.sendall(b"PUT ") 
        
        # Padded headers to maintain fixed length for the server
        folder_header = f"{remote_folder:<32}".encode()
        file_header = f"{filename:<32}".encode()
        
        s.sendall(folder_header)
        s.sendall(file_header)
        
        with open(filename, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                s.sendall(chunk)
    print(f"[+] Uploaded {filename} to {remote_folder}")

if __name__ == "__main__":
    dest_folder = input("Enter remote destination folder name: ")
    user_input = input("Enter local filenames to upload (space separated): ")
    
    for file in user_input.split():
        upload_file(file, dest_folder)