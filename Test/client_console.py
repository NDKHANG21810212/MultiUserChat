import socket   # Tạo kết nối mạng
import threading    # Xử lý đa luồng kết nối nhiều client
import json # Xử lý dữ liệu dạng JSON
HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tạo socket TCP
client_socket.connect((HOST, PORT))

username = input("Nhập tên của bạn: ")
join_package = (json.dumps({"type": "join", "sender": username}) + '\n').encode("utf-8")
client_socket.send(join_package)

print("Đã kết nối tới server. Nhập tin nhắn và Enter để gửi (nhập 'exit' để thoát):")

def recive_messages():
    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                print("Lỗi kết nối.")
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    package = json.loads(line)
                    msg_type = package.get("type")
                    if msg_type == "message":
                        sender = package.get("sender", "Server")
                        message = package.get("message", "")
                        print(f"\n[{sender}]: {message}")
                    elif msg_type == "private":
                        sender = package.get("sender", "Server")
                        message = package.get("message", "")
                        print(f"\n[{sender} -> bạn]: {message}")
                    elif msg_type == "user_list":
                        users = package.get("users", [])
                        print(f"\n[Server]: Danh sách user hiện tại: {users}")
                    elif msg_type == "exit":
                        sender = package.get("sender", "Server")
                        print(f"\n{sender} đã thoát.")
                except json.JSONDecodeError:
                    print(f"\n(Server): {line}")
        except:
            print("Đã ngắt kết nối.")
            break


thread = client_socket_thread = threading.Thread(target=recive_messages,daemon=True)
thread.start()
while True:
  msg = input(">> ")
  if msg.strip() == "":
        continue   # bỏ qua không gửi nếu rỗng
  if msg.lower() == "exit":
        package = json.dumps({"type" :"exit","sender": username}) + '\n'
        client_socket.send(package.encode("utf-8"))
        client_socket.close()
        break
    
  package = (json.dumps({"type" :"message","sender": username,"message": msg}) + '\n').encode("utf-8")
  client_socket.send(package)