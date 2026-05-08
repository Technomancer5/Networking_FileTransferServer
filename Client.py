SERVER_IP = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096

def send_request(command, filename=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        
        # Format command to always be 4 bytes
        header = f"{command:<4}".encode()
        s.sendall(header)

        if command == "PING":
            response = s.recv(BUFFER_SIZE).decode()
            print(f"Server says: {response}")

        elif command == "LIST":
            response = s.recv(BUFFER_SIZE).decode()
            print("Files on server:\n" + response)

        elif command == "PUT" and filename:
            with open(filename, "rb") as f:
                while chunk := f.read(BUFFER_SIZE):
                    s.sendall(chunk)
            print(f"[+] Uploaded {filename}")

if __name__ == "__main__":
    # Example usage
    send_request("PING")
    send_request("LIST")
    # send_request("PUT", "test_file.txt")