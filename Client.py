import socket
import os

SERVER_IP, PORT, BUFFER_SIZE = '192.168.1.171', 65432, 4096

def upload_logic(filename, folder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.sendall(b"PUT ")
        s.sendall(f"{folder:<32}".encode())
        s.sendall(f"{filename:<32}".encode())

        # Wait for Server status
        status = s.recv(6).decode().strip()
        if status == "EXISTS":
            choice = input(f"[?] {filename} already exists. Overwrite? (y/n): ").lower()
            if choice == 'y':
                sure = input(f"    ARE YOU SURE you want to overwrite {filename}? (y/n): ").lower()
                if sure == 'y':
                    s.sendall(b"PROCEED")
                else:
                    s.sendall(b"CANCEL ")
                    return
            else:
                s.sendall(b"CANCEL ")
                return
        
        # Stream file in 4KB chunks [3, 4]
        with open(filename, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                s.sendall(chunk)
    print(f"[+] {filename} upload complete.")

if __name__ == "__main__":
    dest_folder = input("Enter remote destination folder: ")
    
    # Generate Numbered List [6]
    local_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print("\nLocal Files:")
    for i, name in enumerate(local_files, 1):
        print(f"{i}. {name}")
    print("A. Upload ALL files")

    selection = input("\nEnter file numbers (e.g. 1 3), or 'A' for all: ").strip().upper()
    
    files_to_send = []
    if selection == 'A':
        files_to_send = local_files
    else:
        indices = [int(x) - 1 for x in selection.split() if x.isdigit()]
        files_to_send = [local_files[i] for i in indices if 0 <= i < len(local_files)]

    for file in files_to_send:
        upload_logic(file, dest_folder)