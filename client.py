from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

connection_port = 1025
data_port = 1024
server_host = ''


def main():
    connection_socket = socket(AF_INET, SOCK_STREAM)
    # two parentheses due to connect() only accepting one argument and requiring a tuple
    connection_socket.connect((server_host, connection_port))

    data = "Hello World!"
    data_length = len(data)

    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.connect((server_host, data_port))
    data_socket.send(str(data_length))

    #to keep second data transmission (data) from being part of first (data_length)
    sleep(0.005)

    data_sent = 0

    while data_sent != len(data):
        data_sent += data_socket.send(data[data_sent])
    data_socket.close()
    connection_socket.close()

if __name__ == '__main__':
    main()