import json
import socket
from threading import Thread
from websocket_server import WebsocketServer # <-- Thư viện mới

# --- Config ---
TCP_HOST = '127.0.0.1'
TCP_PORT = 12345 # Port của server.py
WS_HOST = '127.0.0.1'
WS_PORT = 8765 # Port cho trình duyệt

print(f"Khởi động Gateway (dùng Threading)... Lắng nghe trên {WS_HOST}:{WS_PORT}")
print(f"Gateway sẽ kết nối tới TCP Server tại {TCP_HOST}:{TCP_PORT}")

#    (Đọc tin từ server.py và gửi cho 1 trình duyệt cụ thể)
def tcp_to_ws(tcp_sock, ws_client, ws_server):
    try:
        buffer = ""
        while True:
            # Đọc từ server.py 
            data = tcp_sock.recv(1024).decode('utf-8')
            if not data:
                break # Server TCP ngắt kết nối
            
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                # Gửi tin nhắn (line) cho 1 client trình duyệt cụ thể
                ws_server.send_message(ws_client, line) 
    except Exception as e:
        print(f"[Gateway TCP-Reader] Lỗi: {e}")
    finally:
        print(f"[Gateway TCP-Reader] Ngắt kết nối với {ws_client['address']}")
        tcp_sock.close()


# 1. Callback: Khi có 1 trình duyệt mới kết nối
def new_client(client, server):
    print(f"[Gateway WS] Trình duyệt mới kết nối: {client['address']}")
    try:
        # 1. Tạo 1 kết nối TCP MỚI tới server.py
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((TCP_HOST, TCP_PORT))
        print(f"[Gateway] Đã kết nối tới TCP Server cho {client['address']}")
        
        # 2. Lưu socket TCP này vào client để dùng ở các hàm callback khác
        client['tcp_socket'] = tcp_client

        # 3. Tạo 1 luồng (thread) để đọc tin từ TCP server và gửi cho client này
        t = Thread(target=tcp_to_ws, args=(tcp_client, client, server), daemon=True)
        t.start()
        
    except Exception as e:
        print(f"[Gateway] Lỗi: Không thể kết nối tới TCP Server (server.py): {e}")
        # Nếu không kết nối được, ta phải ngắt kết nối trình duyệt này
        # (Cách này hơi xấu nhưng thư viện này không cho API 'close()')
        client['handler'].keep_alive = False


# 2. Callback: Khi trình duyệt ngắt kết nối
def client_left(client, server):
    # Kiểm tra xem client có phải là None không (do handshake thất bại)
    if not client:
        print("[Gateway WS] Một kết nối không xác định đã ngắt (lỗi handshake).")
        return # Dừng hàm tại đây
    print(f"[Gateway WS] Trình duyệt đã ngắt kết nối: {client.get('address', 'unknown')}")
    try:
        # Đóng kết nối TCP tương ứng
        tcp_sock = client.get('tcp_socket')
        if tcp_sock:
            tcp_sock.close() # Luồng tcp_to_ws sẽ tự động dừng
    except Exception as e:
        print(f"[Gateway] Lỗi khi đóng TCP socket: {e}")

# 3. Callback: Khi nhận được tin nhắn từ trình duyệt (WS)
def message_received(client, server, message):
    # 'message' là chuỗi JSON từ trình duyệt
    try:
        # Lấy socket TCP đã lưu
        tcp_sock = client['tcp_socket']
        
        # Gửi tin nhắn đó vào server.py (nhớ thêm \n)
        tcp_sock.sendall((message + '\n').encode('utf-8'))
    except Exception as e:
        print(f"[Gateway] Lỗi khi gửi tin tới TCP Server: {e}")

# Hàm khởi động Gateway server
def start_gateway_server():
    # Khởi tạo server WebSocket
    server = WebsocketServer(host=WS_HOST, port=WS_PORT)
    
    # Gán các hàm callback
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    
    # Chạy vĩnh viễn (giống server.py)
    server.run_forever()

# Khối này để bạn có thể chạy file này độc lập
if __name__ == "__main__":
    start_gateway_server()