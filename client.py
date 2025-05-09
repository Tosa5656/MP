import socket
import threading
import sys
import webbrowser
from time import sleep

def show_menu():
    print("╔══════════════════════════════════╗")
    print("║        МЕНЮ ВЫБОРА               ║")
    print("╠══════════════════════════════════╣")
    print("║ 1. Подключиться к чату           ║")
    print("║ 2. Перейти на GitHub репозиторий ║")
    print("║ 3. Выход                         ║")
    print("╚══════════════════════════════════╝")

def clear_last_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            clear_last_line()
            print(f"\n{message}")
            sys.stdout.write("Ваше сообщение: ")
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

def main():
    while True:
        show_menu()
        choice = input("Выберите действие (1-3): ")
        
        if choice == "1":
            target_host = input("Введите IP сервера (по умолчанию 127.0.0.1): ") or '127.0.0.1'
            start_client(target_host)
        elif choice == "2":
            print("Открываю GitHub репозиторий...")
            webbrowser.open("https://github.com/Tosa5656/MP")
        elif choice == "3":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуйте снова")
        
        if choice in ("1", "2"):
            input("\nНажмите Enter чтобы вернуться в меню...")

if __name__ == "__main__":
    main()