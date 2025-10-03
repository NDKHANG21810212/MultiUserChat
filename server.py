import socket #  tạo kết nối mạng
import threading # xử lý đa luồng kết nối nhiều client
HOST = '127.0.0.1'
PORT = 12345

sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_STREAM = Tạo socket TCP
sever_socket.bind((HOST, PORT))
sever_socket.listen()
print('Server is listening on port', PORT) #  mở port khởi động kết nối
client_sockets = [] #Lưu trữ các kết nối client
def broadcast(message, sender_socket = None,sender_addr=None): # Gửi tin nhắn đến tất cả các client trừ người gửi
    for client_socket in list(client_sockets):
        if client_socket != sender_socket: # không gửi lại cho chính nó
            try:
                client_socket.send(f"[{sender_addr}] {message}".encode('utf-8'))
            except:
                    # nếu không gửi được thì ngắt kết nối
                if client_socket in client_sockets:
                    client_sockets.remove(client_socket)
                try:
                    client_socket.close()
                except:
                    pass

def handle_client(client_socket, addr): # Xử lý kết nối client
  print(f'✅ client {addr} connected')
  client_sockets.append(client_socket)
  try: 
     while True:
      message = client_socket.recv(1024).decode('utf-8') #  nhận dữ liệu từ client
       #  nếu không nhận được dữ liệu thì ngắt kết nối
      if not message:
        print(f'❌ client {addr} disconnected')
        break
      print( f'Received from {addr}:', message)
      broadcast(message, client_socket,addr) # Gửi tin nhắn đến tất cả các client trừ người gửi
  except Exception as e:
        print(f'Error handling client {addr}:', e) # lỗi kết nối
  finally:
        if client_socket in client_sockets:
            client_sockets.remove(client_socket)
        try:
            client_socket.close() 
        except:
            pass
        print(f'❌ client {addr} disconnected')
        broadcast(f'Client {addr} has disconnected.',sender_addr="Server") # Thông báo ngắt kết nối đến tất cả các client
while  True:
  client_socket, addr = sever_socket.accept() # Chấp nhận kết nối từ client
  client_thread = threading.Thread(target=handle_client, args=(client_socket,addr)) # Tạo luồng mới để xử lý kết nối client
  client_thread.start()