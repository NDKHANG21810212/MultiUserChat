import socket   # Tạo kết nối mạng
import threading    # Xử lý đa luồng kết nối nhiều client
HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tạo socket TCP
client_socket.connect((HOST, PORT))

print("Đã kết nối tới server. Nhập tin nhắn và Enter để gửi (nhập 'exit' để thoát):")

def recive_messages():
    while True:
        try: 
            msg = client_socket.recv(1024).decode("utf-8")
            if not msg:
                print("Lỗi Kết nối.")
                break
            print("\nServer:", msg)
        except:
            print("Đã ngắt kết nối.")
            break

thread = client_socket_thread = threading.Thread(target=recive_messages,daemon=True)
thread.start()
while True:
  msg = input("> ")
  if msg.strip() == "":
        continue   # bỏ qua không gửi nếu rỗng
  if msg.lower() == "exit":
        print("Đã thoát")
        client_socket.close()
        break
   
  client_socket.send(msg.encode("utf-8"))