import socket
import os
import threading

# --- 1. Conditional Progress Bar Support ---
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("[!] tqdm library not found. Falling back to text-based updates.")

# --- Configuration ---
PORT = 65432
BUFFER_SIZE = 4096 # For the "Big File" problem [3]
BUILT_IN_IPS = ["127.0.0.1", "192.168.1.171", "192.168.1.246"] # Option A list

# --- Server Logic (Background Receiver) ---
def start_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                command = conn.recv(4).decode().strip().upper()
                if command == "PUT":
                    folder = conn.recv(32).decode().strip()
                    filename = conn.recv(32).decode().strip()
                    
                    # Ensure folder exists (client handles the "ask" part)
                    os.makedirs(folder, exist_ok=True) 
                    full_path = os.path.join(folder, filename)
                    
                    with open(full_path, "wb") as f:
                        while chunk := conn.recv(BUFFER_SIZE):
                            f.write(chunk)
                    print(f"\n[+] Received {filename} in {folder} from {addr}")

# --- Client Logic (Interactive Sender) ---
def upload_file(peer_ip, filename, folder):
    filesize = os.path.getsize(filename)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_ip, PORT))
        s.sendall(b"PUT ")
        s.sendall(f"{folder:<32}".encode())
        s.sendall(f"{filename:<32}".encode())

        # Progress Bar Logic [2]
        if TQDM_AVAILABLE:
            with tqdm(total=filesize, unit='B', unit_scale=True, desc=filename, 
                      bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}',
                      ascii=" oC") as pbar:
                with open(filename, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        s.sendall(chunk)
                        pbar.update(len(chunk))
        else:
            print(f"[*] Uploading {filename}...")
            with open(filename, "rb") as f:
                while chunk := f.read(BUFFER_SIZE):
                    s.sendall(chunk)
    print(f"[+] {filename} finished.")

def sender_menu():
    while True:
        print("\n--- IP Selection Menu ---")
        print("A: Choose from Built-in IPs")
        print("B: Manually Enter IP")
        print("C: Map Network (Simple List) & Enter")
        choice = input("Select an option: ").upper()

        target_ip = ""
        if choice == "A":
            for i, ip in enumerate(BUILT_IN_IPS, 1):
                print(f"{i}. {ip}")
            idx = int(input("Select number: ")) - 1
            target_ip = BUILT_IN_IPS[idx]
        elif choice == "B":
            target_ip = input("Enter target IP: ")
        elif choice == "C":
            # Simple local discovery is difficult without a 'Matchmaker' [4].
            # For now, it prompts for manual entry after displaying local info [5].
            os.system('ip addr' if os.name != 'nt' else 'ipconfig')
            target_ip = input("\nEnter IP from mapped list above: ")

        dest_folder = input("Enter destination folder: ")
        
        # --- Folder Confirmation [6] ---
        # Note: In P2P, the client asks locally, then the server acts.
        if not os.path.exists(dest_folder):
            create_choice = input(f"[?] Folder '{dest_folder}' doesn't exist. Create it? (y/n): ").lower()
            if create_choice != 'y':
                print("[!] Upload cancelled.")
                continue

        local_files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for i, name in enumerate(local_files, 1):
            print(f"{i}. {name}")
        
        selection = input("Enter file number or 'A' for all: ").upper()
        files_to_send = local_files if selection == 'A' else [local_files[int(x)-1] for x in selection.split()]

        for file in files_to_send:
            upload_file(target_ip, file, dest_folder)

if __name__ == "__main__":
    threading.Thread(target=start_receiver, daemon=True).start()
    sender_menu()