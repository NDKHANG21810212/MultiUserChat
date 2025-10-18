import threading
import sys
import time
import http.server
import socketserver
import os         # Thêm thư viện 'os'
import functools  # Thêm thư viện 'functools'

# Import 2 hàm server của bạn
from TCP_Server.server import start_tcp_server
from TCP_Server.gateway import start_gateway_server

# --- HÀM 1: KHỞI ĐỘNG HTTP WEB SERVER (ĐÃ SỬA) ---
def start_http_server():
    """Hàm này phục vụ các file (index.html, rooms.html) từ thư mục Web_Client/"""
    PORT = 8000 # Port 8000 là port web phổ biến
    
    # === PHẦN SỬA ĐỔI ===
    # 1. Chỉ định thư mục Web_Client/
    # Lấy đường dẫn đến thư mục chứa file main.py
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Tạo đường dẫn đến thư mục Web_Client/
    web_dir = os.path.join(root_dir, 'Web_Client') #
    
    if not os.path.isdir(web_dir):
        print(f"Lỗi: Không tìm thấy thư mục '{web_dir}'")
        print("Vui lòng tạo thư mục Web_Client/ và đặt index.html, rooms.html vào đó.")
        return

    print(f"HTTP Server sẽ phục vụ file từ: {web_dir}")

    # 2. Tạo Handler để phục vụ từ thư mục đó (thay vì thư mục gốc)
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=web_dir
    )
    # === HẾT SỬA ĐỔI ===

    # Tạo một server HTTP có hỗ trợ đa luồng (threading)
    class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        daemon_threads = True # Tự tắt thread con khi main tắt
        allow_reuse_address = True # Cho phép tái sử dụng port nhanh
        pass

    try:
        # Lắng nghe trên '0.0.0.0' để máy thật và máy ảo đều truy cập được
        httpd = ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
        
        print(f"HTTP Web Server đang chạy.")
        print(f"==> Bạn có thể truy cập tại: http://<IP_MAY_BAN>:{PORT}")
        httpd.serve_forever()
    except OSError as e:
        print(f"Lỗi: Không thể khởi động HTTP Server trên port {PORT}.")
        print("Có thể port 8000 đang bị chiếm (do dịch vụ khác).")
        print(e)
# --- Hết hàm 1 ---


# --- HÀM 2: HÀM MAIN CHÍNH ĐỂ CHẠY CẢ 3 SERVER ---
if __name__ == "__main__":
    print("Khởi động hệ thống MultiUserChat...")
    
    # 1. Chạy TCP server
    print("-> Đang khởi động TCP Server...")
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()
    time.sleep(0.5) # Đợi 0.5s

    # 2. Chạy Gateway
    print("-> Đang khởi động WebSocket Gateway...")
    gateway_thread = threading.Thread(target=start_gateway_server, daemon=True)
    gateway_thread.start()
    time.sleep(0.5) # Đợi 0.5s
    
    # 3. Chạy HTTP Server (MỚI)
    print("-> Đang khởi động HTTP Web Server...")
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    print("\n=== TẤT CẢ 3 SERVER ĐANG CHẠY ===")
    print(f"   TCP Server (cho chat): 0.0.0.0:12345")
    print(f"   WS Gateway (cho web):  0.0.0.0:8765")
    print(f"   HTTP Server (trang): http://<IP_MAY_BAN>:8000")
    print("\nNhấn Ctrl+C để dừng tất cả...")
    
    try:
        while True:
            time.sleep(1) # Giữ cho chương trình chạy
    except KeyboardInterrupt:
        print("\n🛑 Đã nhận tín hiệu Ctrl+C, đang dừng chương trình...")
        sys.exit(0)