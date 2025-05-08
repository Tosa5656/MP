import socket
import threading

clients = []  # Список всех подключённых клиентов

def handle_client(client_socket, addr):
    clients.append(client_socket)  # Добавляем нового клиента
    print(f"[+] Подключен {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{addr[0]}] {message}")
            # Рассылаем сообщение ВСЕМ клиентам, кроме отправителя
            for client in clients:
                if client != client_socket:
                    client.send(message.encode('utf-8'))
        except:
            break
    print(f"[-] Отключен {addr}")
    clients.remove(client_socket)  # Удаляем при отключении
    client_socket.close()

def start_server(host='0.0.0.0', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[*] Сервер слушает {host}:{port}")
    
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
