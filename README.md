# 🗨️ Multi-User Chat (Python Socket)

Ứng dụng chat nhiều người dùng đơn giản viết bằng **Python** sử dụng `socket` và `threading`.

---

## 🚀 Yêu cầu cài đặt

1. **Cài Python**
   - Tải Python tại: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Khi cài đặt nhớ tick **Add Python to PATH** để chạy được lệnh `python` trong terminal.
   - Kiểm tra sau khi cài:
     ```bash
     python --version
     ```

2. **Clone hoặc tải project về**
   - Clone từ GitHub:
     ```bash
     git clone <link-repo>
     ```
   - Hoặc tải file `.zip` rồi giải nén.

3. **Không cần cài thư viện ngoài** (chỉ dùng thư viện chuẩn có sẵn trong Python).

---

## 📂 Cấu trúc dự án
```
MultiUserChat/
│
├── server.py      # Chương trình server
├── client.py      # Chương trình client
└── README.md      # Tài liệu hướng dẫn
```

---

## ▶️ Cách chạy

### 1. Chạy server
Mở terminal tại thư mục `MultiUserChat` và chạy:

```bash
python server.py
```

Nếu thành công sẽ thấy:

```
Server is listening on port 12345
```

---

### 2. Chạy client
Mở thêm **1 hoặc nhiều terminal khác** để chạy client:

```bash
python client.py
```

Kết quả khi kết nối:

```
Đã kết nối tới server. Nhập tin nhắn và Enter để gửi (nhập 'exit' để thoát):
>
```

Gõ tin nhắn và Enter để gửi.  
Gõ `exit` để thoát client.

---

## 💡 Chức năng
- Server có thể phục vụ **nhiều client cùng lúc**.
- Khi một client gửi tin nhắn, server sẽ **phát (broadcast)** đến tất cả client khác.
- Nếu client thoát → server sẽ thông báo cho các client còn lại.

---

## 📝 Ví dụ

### Terminal 1 (server):
```
Server is listening on port 12345
✅ client ('127.0.0.1', 64674) connected
Received from ('127.0.0.1', 64674): hello
```

### Terminal 2 (client 1):
```
Đã kết nối tới server. Nhập tin nhắn và Enter để gửi (nhập 'exit' để thoát):
> hello
Server: [('127.0.0.1', 64678)] hi
```

### Terminal 3 (client 2):
```
Đã kết nối tới server. Nhập tin nhắn và Enter để gửi (nhập 'exit' để thoát):
> hi
Server: [('127.0.0.1', 64674)] hello
```

---

## 👨‍💻 Nhóm thực hiện
- Thành viên A
- Thành viên B
- Thành viên C

---

## ⚠️ Lưu ý
- Server phải được chạy trước, sau đó client mới kết nối được.
- Khi client đóng cửa sổ hoặc `exit`, server sẽ ghi log `disconnected`.
- Port mặc định: `12345` – có thể đổi trong code.

---

## 🐞 Lỗi thường gặp

- **WinError 10054**: client đóng đột ngột → bỏ qua, server sẽ log lại.
- **OSError: [WinError 10048] Address already in use**: Port `12345` đang bị chiếm → đổi số port trong code hoặc tắt chương trình khác đang dùng port.
- **Client không kết nối được**: Kiểm tra firewall, hoặc chắc chắn server đã chạy trước.
