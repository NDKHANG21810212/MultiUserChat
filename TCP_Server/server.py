import socket #  tạo kết nối mạng
import threading # xử lý đa luồng kết nối nhiều client
import json # Xử lý dữ liệu dạng JSON
from datetime import datetime
from threading import Lock 


HOST = '127.0.0.1'
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_STREAM = Tạo socket TCP
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server is listening on port', PORT) #  mở port khởi động kết nối

client_sockets = [] #Lưu trữ các kết nối client
client_name = {} # Lưu trữ tên các client
username_to_socket = {} # Lưu trữ ánh xạ tên người dùng tới socket
lock = threading.Lock()

def get_timestamp():
    return datetime.now().strftime('%H:%M:%S')

def send_to_client(client_socket, message, msg_type="info",sender = "Server"):
    data = json.dumps({
       "type": msg_type,
       "sender": sender,
       "message": message,
       "timestamp": get_timestamp()
    }).encode('utf-8') + b'\n'
    try: 
        client_socket.sendall(data)
        return True
    except:
        return False

def send_private_message(from_socket, to_username, message):
    from_username = None
    with lock:
        for uname, sock in username_to_socket.items():
            if sock == from_socket:
                from_username = uname
                break
    if not from_username:
        from_username = "Unknown"
    
    with lock:
        target_socket = username_to_socket.get(to_username)
    if not target_socket:
        send_to_client(from_socket, f"User {to_username} not found.", msg_type="error")
        return False

    data = json.dumps({
        "type":"private",
        "sender": from_username,
        "message": message,
        "timestamp": get_timestamp()
    }).encode('utf-8') + b'\n'
    try:
        target_socket.sendall(data)
        send_to_client(from_socket, f"Private message sent to {to_username}: {message}.", "private_sent")
        print(f"[{get_timestamp()}] {from_username} to {to_username}: {message}")
        return True
    except:
        send_to_client(from_socket, f"Failed to send private message to {to_username}.", msg_type="error" )
        return False
    
def broadcast_user_list(): # Gửi danh sách người dùng hiện tại cho tất cả client
    with lock:
        users = list(client_name.values())
    data = json.dumps({
    "type": "user_list",
    "users": users,
    "count": len(users),
    "timestamp": get_timestamp()
    }).encode('utf-8') + b'\n'
    with lock:
        for client_socket in client_sockets[:]:
            try: 
                client_socket.sendall(data)
            except:
                pass

def broadcast(message, sender_socket=None, sender_addr=None):
    data = json.dumps({
        "type": "message",
        "sender": str(sender_addr) if sender_addr else "Server",
        "message": message,
        "timestamp": get_timestamp() 
    }).encode('utf-8') + b'\n'
    
    remove_list = []
    with lock:
        for client_socket in client_sockets[:]:
           # if client_socket != sender_socket:
                try:
                    client_socket.sendall(data)
                except (OSError, ConnectionResetError, BrokenPipeError):
                    remove_list.append(client_socket)
    if remove_list:
        with lock:
            for s in remove_list:
                if s in client_sockets:
                    client_sockets.remove(s)
                addr_to_remove = None
                for addr, name in client_name.items():
                    if username_to_socket.get(name) == s:
                        addr_to_remove = addr
                        break
                if addr_to_remove:
                    client_name.pop(addr_to_remove, None)
                       
                for uname, sock in list(username_to_socket.items()):
                    if sock == s:
                        username_to_socket.pop(uname, None)
                        break
                try:
                    s.close()
                except:
                    pass
        if remove_list:
            broadcast_user_list()  # Cập nhật danh sách người dùng sau khi có người thoát

def handle_client(client_socket, addr):  # Xử lý kết nối client
    username = f"User_{addr[0]}_{addr[1]}"  # ✅ Gán giá trị mặc định   
    client_added = False
    try:
        join_data = client_socket.recv(1024).decode('utf-8')  # Nhận dữ liệu đầu tiên
        join_json = json.loads(join_data)
        if join_json.get("type") == "join":
            username = join_json.get("sender", username)
        with lock:
            client_name[addr] = username
            client_sockets.append(client_socket)
            username_to_socket[username] = client_socket
            client_added = True
        print(f'✅ [{get_timestamp()}] {username} {addr} connected')
        broadcast(f"Client {username} has joined the chat.", sender_addr="Server")
        send_to_client(client_socket, f"Welcome {username}! You are connected to the server." f" There are currently {len(client_sockets)} users online.", msg_type="info" )
        broadcast_user_list()  # Gửi danh sách người dùng hiện tại cho tất cả client
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print(f'❌ [{get_timestamp()}] {username} disconnected')
                    break

                package = json.loads(message)
                msg_type = package.get("type")

                if msg_type == "message": # Xử lý tin nhắn
                    sender = package.get("sender", str(addr))
                    msg = package.get("message", "").strip()
                    if not msg:
                        continue  # bỏ qua tin nhắn rỗng
                    if msg.startswith("@"): # Tin nhắn riêng tư
                        parts = msg.split(" ", 1)
                        if len(parts) == 2:
                            to_user = parts[0][1:]  # Tên người nhận (bỏ qua ký tự @)
                            private_msg = parts[1]  # Nội dung tin nhắn
                            send_private_message(client_socket, to_user, private_msg)
                        else:
                            send_to_client(client_socket, "Invalid private message format. Use @username message", msg_type="error")
                    else: # Tin nhắn công khai
                        print(f'[{get_timestamp()}] {username}: {msg}')
                        broadcast(msg, sender_socket=client_socket, sender_addr=username)
                elif msg_type == "exit": # Xử lý thoát
                    sender = package.get("sender", str(addr))
                    print(f'❌ client {username} ({sender}) disconnected')
                    broadcast(f"{username} đã thoát khỏi phòng chat.", sender_addr="Server")
                    with lock:
                        if client_socket in client_sockets:
                            client_sockets.remove(client_socket)
                            client_name.pop(addr, None)
                            username_to_socket.pop(username, None)
                    broadcast_user_list()
                    break
            except json.JSONDecodeError as e:
                print(f"Received non-JSON message from {addr}: {message}")
                continue
            except ConnectionResetError:
                print("Client has disconnected unexpectedly.")
                with lock:
                    if client_socket in client_sockets:
                        client_sockets.remove(client_socket)
                    client_name.pop(addr, None)
                    username_to_socket.pop(username, None)
                    # Broadcast cho các client còn lại
                broadcast(f"Client {username} mất kết nối đột ngột", sender_addr="Server")
                broadcast_user_list()
                break
            except OSError as e:
                print(f"❌ Client {username} socket error: {e}")
                break
    finally:
       if client_added:
        with lock:
            if client_socket in client_sockets:
                client_sockets.remove(client_socket)
            client_name.pop(addr, None)
            username_to_socket.pop(username, None)
            try:
                client_socket.close()
            except:
                pass
           
          
try:
    while  True:
        client_socket, addr = server_socket.accept() # Chấp nhận kết nối từ client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,addr)) # Tạo luồng mới để xử lý kết nối client
        client_thread.daemon = True
        client_thread.start()
except KeyboardInterrupt:
        print("\n🛑 Server shutting down...")
finally:
        server_socket.close()