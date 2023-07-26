import socket
import logging

# Логирование работы программы логирования ^_^
logging.basicConfig(filename="Rose_Wind__len_test.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s') 

server_host = "192.168.54.123"  # Замените на IP-адрес вашего сервера
server_port = 8001  # Замените на порт сервера
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

message = b'\x01\x03\x00\x00\x00\x07\x04\x08'

def receive_data_from_server(host, port):
    client_socket.send(message)
    data = client_socket.recv(1024)
    decoded_data = data.hex()    # Предполагаем, что сервер отправляет текст в кодировке utf-8
    lines = decoded_data.splitlines()
    return lines

if __name__ == "__main__":
    while True:
        try:
            received_lines = receive_data_from_server(server_host, server_port)
            for line in received_lines:
                logging.info(f'{len(line)}, {line}')
                print(len(line), line)
        except socket.error as se:
            logging.error(f"Socket error occurred: {se}")
            
        except socket.timeout as te:
            logging.error(f"Socket timeout occurred: {te}")

