import socket
import os
import platform
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
BUFFER_SIZE = 4096 # Essential for the "Big File" problem [4]
# Sub-menu A Data: Peer metadata
BUILT_IN_PEERS = [
    {"ip": "127.0.0.1", "name": "Local Loopback", "os": platform.system()},
    {"ip": "192.168.1.171", "name": "Garuda - Daily-Driver", "os": "Linux"},
    {"ip": "192.168.1.246", "name": "Mac Mini - Monterey", "os": "Apple"}
]

def get_local_ip():
    """Pulls the local PC's IP address [2]"""
    return socket.gethostbyname(socket.gethostname())

def get_common_paths():
    """Generates relative shortcuts for the peer to resolve"""
    return {
        "1": ("Downloads", "Downloads"), # Tuple Index 0 is label, Index 1 is value
        "2": ("Pictures", "Pictures"),
        "3": ("Videos", "Videos"),
        "M": ("Manual Entry", "MANUAL"),
        "R": ("Remote Explorer", "REMOTE")
    }

# --- Server Logic (Background Receiver) ---
def start_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                # Receive 4-byte command [2]
                command = conn.recv(4).decode().strip().upper()
                
                if command == "LIST":
                    # Remote navigation: send list of files in requested path
                    path = conn.recv(1024).decode().strip()
                    path = os.path.expanduser(path)
                    try:
                        files = "\n".join(os.listdir(path))
                        conn.sendall(files.encode() if files else b"Empty")
                    except:
                        conn.sendall(b"Error: Invalid Path")

                elif command == "PUT":
                    # Receive the folder name and filename from the sender
                    folder = conn.recv(32).decode().strip()
                    filename = conn.recv(32).decode().strip()
                    
                    # NEW: Resolve the path locally on the Receiver (Mac)
                    # This turns "Downloads" into "/Users/yourmacname/Downloads" [1]
                    target_dir = os.path.expanduser(os.path.join("~", folder))
                    os.makedirs(target_dir, exist_ok=True)
                    
                    full_path = os.path.join(target_dir, filename)
                    
                    # Receive the file in 4096-byte chunks to prevent RAM crashes [3, 4]
                    with open(full_path, "wb") as f:
                        while chunk := conn.recv(BUFFER_SIZE):
                            f.write(chunk)

# --- Client Logic (Interactive Sender) ---
def upload_file(peer_ip, filename, folder):
    filesize = os.path.getsize(filename)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_ip, PORT))
        s.sendall(b"PUT ")
        s.sendall(f"{folder:<32}".encode())
        s.sendall(f"{filename:<32}".encode())

        if TQDM_AVAILABLE:
            with tqdm(total=filesize, unit='B', unit_scale=True, desc=filename, 
                      bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}',
                      ascii=" oC") as pbar:
                with open(filename, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        s.sendall(chunk)
                        pbar.update(len(chunk))
        else:
            with open(filename, "rb") as f:
                while chunk := f.read(BUFFER_SIZE):
                    s.sendall(chunk)
    print(f"[+] {filename} upload complete.")

def sender_menu():
    print(f"--- YOUR LOCAL IP: {get_local_ip()} ---") # Requirement: IP on first line
    print("Ready for file transfer or run this on another PC and select an option below.") # Requirement: Header instructions
    
    while True:
        print("\n--- IP Selection Menu ---")
        print("A: Choose from Built-in IPs")
        print("B: Manually Enter IP")
        print("C: Map Network (Simple List) & Enter")
        choice = input("Select an option: ").upper()

        target_ip = ""
        if choice == "A":
            print("\n--- TRUSTED PEERS ---")
            for i, p in enumerate(BUILT_IN_PEERS, 1):
                print(f"{i}. {p['name']} ({p['ip']}) - OS: {p['os']}") # Requirement: Sub-menu with Name/OS
            target_ip = BUILT_IN_PEERS[int(input("Select number: "))-1]['ip']
        elif choice == "B":
            target_ip = input("Enter target IP: ")

        # --- Destination Pathing Logic ---
        paths = get_common_paths()
        print("\n--- DESTINATION FOLDER ---")
        for k, v in paths.items():
            if k not in ["M", "R"]: 
                # This joins every item found in the tuple with " - "
                # It won't crash regardless of how many items are in 'v'
                display_text = " - ".join(v)
                print(f"{k}. {display_text}")

        print("M. Manual Entry (Use ~ for Home)")
        print("R. Remote Explorer (See what's on the other PC)")
        
        p_choice = input("Select option: ").upper()
        
        if p_choice == "M":
            # REMOVED: os.path.expanduser(...)
            # ADDED: Raw input string
            dest_folder = input("Enter path (e.g., ~/Desktop): ") 
            
        elif p_choice == "R":
            # (Your Remote Explorer logic remains here)
            pass

        elif p_choice == "C":
            # NEW: Logic for "Map Network (Simple List) & Enter"
            print("\n--- KNOWN PEERS ---")
            for i, peer in enumerate(BUILT_IN_PEERS, 1):
                # Pulls Name, OS, and IP from your metadata list [1]
                print(f"{i}. {peer['name']} [{peer['os']}] - {peer['ip']}")
            
            p_idx = int(input("Select peer number: ")) - 1
            target_ip = BUILT_IN_PEERS[p_idx]['ip']
            print(f"[!] Target set to: {target_ip}")
            continue # Returns to menu to pick the folder/files now

        else:
            dest_folder = paths[p_choice][1]

        # New direct path to file selection:
        local_files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for i, name in enumerate(local_files, 1): 
            print(f"{i}. {name}")
    
        sel = input("Enter number(s) or 'A' for all: ").upper()
        files = local_files if sel == 'A' else [local_files[int(x)-1] for x in sel.split()]

        for f in files: upload_file(target_ip, f, dest_folder)

if __name__ == "__main__":
    # Start the receiver in the background so the menu can run [1]
    threading.Thread(target=start_receiver, daemon=True).start() 
    sender_menu()
