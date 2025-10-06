import socket #  tạo kết nối mạng
import threading # xử lý đa luồng kết nối nhiều client
import json # Xử lý dữ liệu dạng JSON
from threading import Lock

HOST = '127.0.0.1'
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_STREAM = Tạo socket TCP
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server is listening on port', PORT) #  mở port khởi động kết nối

client_sockets = [] #Lưu trữ các kết nối client
client_name = {} # Lưu trữ tên các client

lock = Lock()

def broadcast(message, sender_socket=None, sender_addr=None):
    data = json.dumps({
        "type": "message",
        "sender": str(sender_addr) if sender_addr else "Server",
        "message": message
    }).encode('utf-8')

    with lock:
        for client_socket in client_sockets[:]:
            if client_socket != sender_socket:
                try:
                    client_socket.send(data)
                except:
                    client_sockets.remove(client_socket)
                    client_socket.close()

def handle_client(client_socket, addr):  # Xử lý kết nối client
    username = f"User_{addr[0]}_{addr[1]}"  # ✅ Gán giá trị mặc định NGAY ĐẦU

    try:
        join_data = client_socket.recv(1024).decode('utf-8')  # Nhận dữ liệu đầu tiên
        if not join_data:
            raise ConnectionError("Client disconnected before sending username")

        join_json = json.loads(join_data)
        if join_json.get("type") == "join":
            username = join_json.get("sender", username)
        client_name[addr] = username
        client_sockets.append(client_socket)
        print(f'✅ client {addr} connected as {username}')
        broadcast(f"Client {username} has joined the chat.", sender_addr="Server")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f'❌ client {username} disconnected')
                break

            try:
                package = json.loads(message)
                msg_type = package.get("type")
                if msg_type == "message":
                    sender = package.get("sender", str(addr))
                    msg = package.get("message", "")
                    print(f"[{sender}]: {msg}")
                    broadcast(msg, client_socket, sender_addr=username)
                elif msg_type == "exit":
                    sender = package.get("sender", str(addr))
                    print(f'❌ client {username} ({sender}) disconnected')
                    break

            except json.JSONDecodeError:
                print(f"Received non-JSON message from {addr}: {message}")

    except Exception as e:
        print(f'Error handling client {addr}:', e)

    finally:
        if client_socket in client_sockets:
            client_sockets.remove(client_socket)
        name = client_name.pop(addr, "Unknown")
        try:
            client_socket.close()
        except:
            pass
        print(f'❌ client {addr} ({username}) disconnected')
        broadcast(f'Client {username} has disconnected.', sender_addr="Server")
while  True:
  client_socket, addr = server_socket.accept() # Chấp nhận kết nối từ client
  client_thread = threading.Thread(target=handle_client, args=(client_socket,addr)) # Tạo luồng mới để xử lý kết nối client
  client_thread.start()