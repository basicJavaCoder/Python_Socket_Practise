import socket


def start_client():
    # Connect to the server via socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Server sends menu options + Client displays them to user
    menu = client_socket.recv(1024).decode()
    print(f"\033[1;32m{menu}\033[0m")

    # Get user choice at menu
    choice = input("\033[1;33mEnter your choice: \033[0m")
    client_socket.send(bytes(choice, "utf-8"))

    # Option 6 does not require additional information from Server, so we can check if it is safe to close socket
    if choice != 6:
        # Server asks for Employee ID in order to proceed
        emp_id_request = client_socket.recv(1024).decode()
        emp_id = input(f"\033[95m{emp_id_request}\033[0m")

        # Send Employee ID to server
        client_socket.send(bytes(emp_id, "utf-8"))

        # Server sends response from the function + Print it for the user
        reply = client_socket.recv(1024).decode()
        print(f"\033[94m{reply}\033[0m")

    # Close socket connection to server
    client_socket.close()


if __name__ == "__main__":
    start_client()
