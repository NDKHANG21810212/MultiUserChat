import threading
from TCP_Server.server import start_tcp_server
from TCP_Server.gateway import start_gateway_server

if __name__ == "__main__":
    # Chạy TCP server trong 1 luồng riêng
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()

    # Chạy gateway (Flask / FastAPI / WebSocket server)
    start_gateway_server()