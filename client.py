import socket
import threading
import sys
from time import sleep

def clear_last_line():
    sys.stdout.write("\033[F")  # Переместить курсор на одну строку вверх
    sys.stdout.write("\033[K")  # Очистить строку

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            clear_last_line()  # Очищаем строку ввода
            print(f"{message}")  # Новое сообщение с новой строки
            sys.stdout.write("Ваше сообщение: ")  # Восстанавливаем приглашение
            sys.stdout.flush()
        except:
            print("\nСоединение разорвано!")
            sock.close()
            break

def start_client(host='127.0.0.1', port=5555):
    nickname = input("Введите ваш ник: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    print(f"Подключен к {host}:{port}. Для выхода введите 'exit'")
    while True:
        try:
            message = input("Ваше сообщение: ")
            if message.lower() == 'exit':
                client.close()
                break
            full_message = f"[{nickname}] {message}"
            client.send(full_message.encode('utf-8'))
        except KeyboardInterrupt:
            client.close()
            break
        except:
            break

if __name__ == "__main__":
    target_host = input("Введите IP сервера (по умолчанию 127.0.0.1): ") or '127.0.0.1'
    start_client(target_host)