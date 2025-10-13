🗨️ Multi-User Chat (Python Socket)

Ứng dụng chat nhiều người dùng (multi-user chat) được xây dựng bằng Python, sử dụng lập trình socket TCP và đa luồng (threading) để cho phép nhiều client giao tiếp với nhau thông qua một server trung tâm.

🚀 1. Yêu cầu cài đặt

Cài đặt Python

Tải Python tại: https://www.python.org/downloads/

Khi cài đặt, nhớ tick chọn Add Python to PATH để chạy được lệnh python trong terminal.

Kiểm tra cài đặt:

python --version


Tải hoặc clone project

Clone từ GitHub:

git clone [<link-repo>](https://github.com/NDKHANG21810212/MultiUserChat.git)


Hoặc tải file .zip rồi giải nén ra máy.

Không cần cài thêm thư viện ngoài các thư viện chuẩn có sẵn trong Python (socket, threading, tkinter, json, v.v.).

📁 2. Cấu trúc thư mục dự án
MultiUserChat/
│
├── TCP_Server/
│   ├── __init__.py         # Đánh dấu module Python
│   ├── gateway.py          # (Sẽ dùng sau) - xử lý trung gian / định tuyến gói tin
│   └── server.py           # Chương trình server chính (xử lý nhiều client bằng thread)
│
├── Test/
│   ├── client_console.py   # Client giao diện console (dòng lệnh)
│   └── client_tkinter.py   # Client có giao diện GUI dùng Tkinter
│
├── Web_Client/
│   ├── community.html      # (Chưa triển khai) - giao diện chat cộng đồng
│   ├── index.html          # (Chưa triển khai) - trang chủ
│   ├── private.html        # (Chưa triển khai) - chat riêng tư
│   └── rooms.html          # (Chưa triển khai) - danh sách phòng
│
├── .hintrc                 # Cấu hình gợi ý mã nguồn (nếu dùng code linter)
├── main.py                 # File khởi chạy chính (dùng để gọi server/test)
└── README.md               # Tài liệu hướng dẫn


⚠️ Lưu ý:
Hiện tại dự án đang ở giai đoạn Test GUI (Tkinter), phần gateway.py và Web_Client chưa cần chạy.

▶️ 3. Hướng dẫn chạy thử
🖥️ 1. Chạy Server

Mở terminal tại thư mục gốc của dự án (MultiUserChat) và chạy:

python -m TCP_Server.server


Khi server khởi động thành công, màn hình sẽ hiển thị:

Server is listening on port 12345

💬 2. Chạy Client Console (dòng lệnh)

Mở một terminal khác và chạy:

python Test/client_console.py


Sau khi kết nối thành công:

Đã kết nối tới server. Nhập tin nhắn và Enter để gửi (nhập 'exit' để thoát):
>


Bạn có thể mở nhiều terminal khác nhau để chạy nhiều client cùng lúc.

🪟 3. Chạy Client Tkinter (giao diện đồ họa)

Nếu muốn thử giao diện dạng cửa sổ, chạy:

python Test/client_tkinter.py


Giao diện Tkinter sẽ hiển thị khung chat.

Mỗi cửa sổ Tkinter tương ứng với một người dùng.

Bạn có thể mở nhiều cửa sổ để kiểm tra tính năng chat nhiều người.

Tin nhắn được hiển thị theo phong cách trái-phải, giúp dễ phân biệt người gửi và người nhận.

💡 4. Các chức năng đã hoàn thành

✅ Server TCP hoạt động ổn định, hỗ trợ nhiều client cùng lúc (thread-based).

✅ Client Console có thể gửi và nhận tin nhắn từ các client khác.

✅ Client Tkinter GUI hiển thị tin nhắn với bố cục đẹp, rõ ràng.

✅ Cơ chế broadcast: mỗi tin nhắn gửi đi sẽ được chuyển đến tất cả client khác đang kết nối.

⚙️ Gateway: chuẩn bị cho giai đoạn kết nối web sau này.

🌐 Web Client: đang trong quá trình phát triển (sẽ kết nối qua gateway).

🧪 5. Ví dụ minh họa
Terminal 1 (Server):
Server is listening on port 12345
✅ Client ('127.0.0.1', 64512) connected
Received from ('127.0.0.1', 64512): Hello

Terminal 2 (Client 1):
> Hello
Server broadcast: [User2] Hi there!

Tkinter (Client 2):

Khung chat hiển thị:

[Bạn]: Hello
[User1]: Hi there!

⚠️ 6. Lưu ý sử dụng

Chạy server trước, sau đó mới mở client.

Mặc định port 12345, có thể thay đổi trong server.py.

Nếu client bị đóng đột ngột, server sẽ log disconnected.

Khi muốn thoát, gõ exit (với client console) hoặc đóng cửa sổ (Tkinter).

🐞 7. Lỗi thường gặp
Lỗi	Nguyên nhân	Cách khắc phục
WinError 10054	Client bị ngắt kết nối đột ngột	Bỏ qua, server sẽ tự xử lý
WinError 10048	Port đang bị chiếm	Đổi port hoặc tắt chương trình khác
UnicodeEncodeError	Lỗi font terminal khi nhập tiếng Việt	Dùng Tkinter client hoặc đổi terminal sang UTF-8
Client không kết nối được	Firewall chặn, hoặc server chưa chạy	Kiểm tra firewall hoặc khởi động lại server