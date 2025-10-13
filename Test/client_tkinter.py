import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, simpledialog

HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("💬 Chat Client - Tkinter")
        self.root.geometry("500x400")

        # Hỏi username bằng hộp thoại
        self.username = simpledialog.askstring("Đăng nhập", "Nhập tên của bạn:", parent=root)
        if not self.username:
            self.root.destroy()
            return

        # Kết nối socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        # ===== UI chính =====
        self.text_area = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD, state=tk.DISABLED)
        self.text_area.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        self.msg_entry = tk.Entry(frame, width=40)
        self.msg_entry.grid(row=0, column=0, padx=5)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = tk.Button(frame, text="Gửi", width=10, command=self.send_message)
        self.send_btn.grid(row=0, column=1)

        # Tag để căn trái/phải
        self.text_area.tag_configure("left", justify="left", background="#e6e6e6", lmargin1=10, lmargin2=10, spacing3=5)
        self.text_area.tag_configure("right", justify="right", background="#cce5ff", rmargin=10, spacing3=5)
        self.text_area.tag_configure("system", justify="center", foreground="gray")

        # Gửi join message
        join_msg = {"type": "join", "sender": self.username}
        self.sock.send((json.dumps(join_msg) + "\n").encode("utf-8"))

        # Thread nhận tin nhắn
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        package = {
            "type": "message",
            "sender": self.username,
            "message": msg
        }
        try:
            self.sock.send((json.dumps(package) + "\n").encode("utf-8"))
            self.display_message(f"Bạn: {msg}", "right")
            self.msg_entry.delete(0, tk.END)
        except:
            self.display_message("⚠️ Không thể gửi tin nhắn (mất kết nối)", "system")

    def receive_messages(self):
        buffer = ""
        while True:
            try:
                data = self.sock.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    pkg = json.loads(line)
                    sender = pkg.get("sender", "")
                    message = pkg.get("message", "")
                    if sender != self.username:
                        self.display_message(f"{sender}: {message}", "left")
            except:
                self.display_message("⚠️ Mất kết nối tới server", "system")
                break

    def display_message(self, msg, tag):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, msg + "\n", tag)
        self.text_area.configure(state=tk.DISABLED)
        self.text_area.yview(tk.END)


# === Chạy chương trình ===
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
