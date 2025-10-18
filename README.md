
# 🗨️ Ứng dụng Chat Đa Người Dùng (Multi-User Chat)

### (Python Socket, WebSocket & Web Client)

Ứng dụng chat nhiều người dùng (multi-user chat) được xây dựng bằng Python. Ban đầu, dự án sử dụng lập trình socket TCP và đa luồng (threading) để cho phép nhiều client (Console, Tkinter) giao tiếp với nhau qua một server trung tâm.

Hiện tại, dự án đã được **nâng cấp hoàn chỉnh** thành một hệ thống Web Chat, bao gồm 3 thành phần máy chủ chạy đồng thời:

1.  **TCP Server:** Lõi xử lý logic chat, quản lý kết nối, và broadcast tin nhắn.
2.  **WebSocket Gateway:** Cầu nối "phiên dịch" giữa giao thức WebSocket (từ trình duyệt) và giao thức TCP (của server lõi).
3.  **HTTP Server:** Máy chủ web để phục vụ các file giao diện (`index.html`, `rooms.html`) cho người dùng qua trình duyệt.

Toàn bộ 3 máy chủ này được khởi chạy đồng thời chỉ bằng **một file `main.py` duy nhất**.

-----

## 🚀 1. Yêu cầu cài đặt

1.  **Cài đặt Python**

      * Tải Python tại: `https://www.python.org/downloads/`
      * (Khi cài đặt, nhớ tick chọn `Add Python to PATH` để chạy được lệnh `python` trong terminal).

2.  **Tải hoặc clone project**

git clone [<link-repo>](https://github.com/NDKHANG21810212/MultiUserChat.git)

Hoặc tải file .zip rồi giải nén ra máy.

3.  **Cài đặt thư viện (Bắt buộc)**

      * Dự án này sử dụng một thư viện bên ngoài để làm WebSocket Gateway. Mở terminal và chạy:
    ```
    pip install websocket-server
    ```

-----

## 📁 2. Cấu trúc thư mục dự án

```
MultiUserChat/
│
├── TCP_Server/
│   ├── __init__.py         # Đánh dấu module Python
│   ├── gateway.py          # Cầu nối WebSocket <-> TCP
│   └── server.py           # Lõi Server TCP (xử lý logic chat)
│
├── Test/
│   ├── client_console.py   # Client Console (dùng để test TCP)
│   └── client_tkinter.py   # Client GUI Tkinter (dùng để test TCP)
│
├── Web_Client/
│   ├── index.html          # Trang đăng nhập Web
│   └── rooms.html          # Giao diện phòng chat chính
│
├── main.py                 # File khởi chạy TẤT CẢ 3 server
└── README.md               # Tài liệu hướng dẫn (file này)
```

-----

## ▶️ 3. Hướng dẫn chạy (Web Client - Chính)

Bạn chỉ cần chạy **một file `main.py` duy nhất** để khởi động toàn bộ hệ thống.

### 3.1. Cấu hình Demo (Rất quan trọng)

Trước khi chạy, bạn cần quyết định sẽ demo ở đâu và cấu hình IP cho chính xác.

**A. Nếu demo trên cùng 1 máy (Localhost):**

1.  Sửa file `TCP_Server/server.py`: Đặt `HOST = '127.0.0.1'`.
2.  Sửa file `TCP_Server/gateway.py`: Đặt `WS_HOST = '127.0.0.1'`.
3.  Sửa file `Web_Client/rooms.html`: Đặt `const ws_ip = "127.0.0.1";`.

**B. Nếu demo qua Mạng LAN (1 máy thật, nhiều máy ảo):**

1.  Sửa file `TCP_Server/server.py`: Đặt `HOST = '0.0.0.0'`.
2.  Sửa file `TCP_Server/gateway.py`: Đặt `WS_HOST = '0.0.0.0'`.
3.  Sửa file `Web_Client/rooms.html`: Đặt `const ws_ip = "192.168.x.x";` (thay bằng IP LAN của máy chạy `main.py`).
4.  **Mở Tường lửa (Firewall)** trên máy chủ (máy thật) cho 3 port:
      * `12345` (cho TCP Server)
      * `8765` (cho WebSocket Gateway)
      * `8000` (cho HTTP Server)

### 3.2. Khởi động hệ thống

Mở terminal tại thư mục gốc của dự án (`MultiUserChat/`) và chạy:

```bash
python main.py
```

Khi hệ thống khởi động thành công, màn hình sẽ hiển thị 3 server đã sẵn sàng:

```
Khởi động hệ thống MultiUserChat...
-> Đang khởi động TCP Server...
Server is listening on port 12345
-> Đang khởi động WebSocket Gateway...
Khởi động Gateway (dùng Threading)... Lắng nghe trên 0.0.0.0:8765
-> Đang khởi động HTTP Web Server...
HTTP Server sẽ phục vụ file từ: E:\...\MultiUserChat\Web_Client

=== TẤT CẢ 3 SERVER ĐANG CHẠY ===
   TCP Server (cho chat): 0.0.0.0:12345
   WS Gateway (cho web):  0.0.0.0:8765
   HTTP Server (trang): http://<IP_MAY_BAN>:8000

Nhấn Ctrl+C để dừng tất cả...
```

### 3.3. Truy cập ứng dụng

Mở trình duyệt (Chrome, Firefox...) và truy cập vào địa chỉ của **HTTP Server** (port 8000).

  * **Nếu chạy local:** `http://localhost:8000` (hoặc `http://127.0.0.1:8000`)
  * **Nếu chạy LAN:** `http://192.168.x.x:8000` (IP máy thật)

Bạn sẽ thấy trang đăng nhập (`index.html`). Nhập tên và bắt đầu chat\! Bạn có thể mở nhiều tab trình duyệt hoặc dùng nhiều máy ảo để giả lập nhiều người dùng.

-----

## 🧪 4. Hướng dẫn chạy (Client Test TCP - Tùy chọn)

Nếu bạn không muốn chạy Web Client, bạn vẫn có thể test lõi TCP Server (`server.py`) bằng các client console và Tkinter (như trong đề tài gốc).

**1. Chạy Server TCP (độc lập):**
Mở terminal và chạy:
```bash
python -m TCP_Server.server
```
*Lưu ý: Nếu chạy cách này, Gateway và Web Client sẽ không hoạt động nên không cần chạy 2 file gateway.py và main.py.*

**2. Chạy Client Console (dòng lệnh):**
Mở một terminal khác và chạy:

```bash
python Test/client_console.py
```

**3. Chạy Client Tkinter (giao diện đồ họa):**
Mở một terminal khác và chạy:

```bash
python Test/client_tkinter.py
```

-----

## 💡 5. Các chức năng đã hoàn thành

✅ Lõi Server TCP: Hoạt động ổn định, triển khai chính xác mô hình Client-Server. Sử dụng socket và threading (đa luồng) để xử lý nhiều kết nối client đồng thời, đúng theo yêu cầu đề tài.

✅ Chat Chung (Broadcast): Server có khả năng nhận tin nhắn từ một client và broadcast (phát lại) cho tất cả các client khác đang kết nối.

✅ Chat Riêng Tư: Hoàn thành tính năng nâng cao, cho phép client chat riêng với nhau bằng cú pháp @username. Logic server xử lý chính xác việc tìm kiếm và gửi tin cho đúng người nhận.

✅ Quản lý User (Join/Leave): Xử lý đầy đủ logic khi người dùng tham gia (join), chủ động thoát (exit), và tự động phát hiện ngắt kết nối đột ngột (xử lý try...except).

✅ Hiển thị Danh sách Online: Server tự động gửi danh sách người dùng đang online (cập nhật theo thời gian thực) mỗi khi có người tham gia hoặc rời phòng.

✅ Client Test (Console & Tkinter): Xây dựng thành công 2 client gốc để kiểm thử lõi TCP là client_console.py (dòng lệnh) và client_tkinter.py (giao diện đồ họa)

✅ Mở rộng Web Client (Nâng cao): Xây dựng giao diện web hoàn chỉnh (HTML/CSS/JS) với trang đăng nhập (index.html) và phòng chat (rooms.html) có đầy đủ tính năng.

✅ Hệ thống 3-Server (Nâng cao): Tích hợp và khởi chạy đồng thời cả 3 server (TCP Server, WebSocket Gateway, và HTTP Server) chỉ bằng một file main.py duy nhất.
-----
6. Lỗi thường gặp
Lỗi: WinError 10048 (Address already in use)
Nguyên nhân: Port (12345, 8765, hoặc 8000) đang bị một chương trình khác chiếm.

Cách khắc phục: Đóng chương trình đó (kiểm tra Task Manager) hoặc khởi động lại máy.

Lỗi: WinError 10054 (Connection reset)
Nguyên nhân: Client (web hoặc console) ngắt kết nối đột ngột (ví dụ: đóng tab).

Cách khắc phục: Bỏ qua. Đây là hành vi bình thường, server đã xử lý finally để dọn dẹp.

Lỗi: KeyError: 'upgrade' (Log trong terminal)
Nguyên nhân: Bạn (hoặc trình duyệt) truy cập Gateway (port 8765) bằng http:// thay vì ws:// (WebSocket).

Cách khắc phục: Bỏ qua. Đây là lỗi handshake bình thường. Hãy luôn truy cập qua HTTP Server (port 8000).

Lỗi: Truy cập localhost:8000 hiện danh sách file
Nguyên nhân: main.py không tìm thấy file index.html trong thư mục Web_Client/.

Cách khắc phục: Đảm bảo index.html và rooms.html nằm đúng trong thư mục Web_Client/.

Lỗi: (Demo LAN) Web tải được, nhưng không chat được
Nguyên nhân:

Firewall (Tường lửa) đang chặn port 8765 (WS) hoặc 12345 (TCP).

Biến ws_ip trong rooms.html sai (không phải IP LAN của máy chủ).

Cách khắc phục:

Mở Inbound Rules trong Firewall của máy chủ cho cả 3 port.

Đảm bảo ws_ip là IP LAN của máy chủ (kiểm tra bằng ipconfig).

Lỗi: (Demo LAN) Không tải được web
Nguyên nhân:

Firewall (Tường lửa) đang chặn port 8000 (HTTP).

Bạn gõ sai IP của máy chủ.

Cách khắc phục:

Mở Inbound Rules trong Firewall cho port 8000.

Kiểm tra lại IP (dùng ipconfig trên máy chủ).