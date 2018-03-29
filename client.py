from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep

connection_port = 1025
data_port = 1024
server_host = ''


def main():
    connection_socket = create_connection_socket()
    quit_loop = False
    while not quit_loop:

        ftp_input = get_input()

        if len(ftp_input) == 1:
            quit_loop = len_one_input(ftp_input)
        elif len(ftp_input) == 2:
            len_two_input(ftp_input)
        else:
            print "Unrecognized set of commands"

        #to give connection_socket time to connect
        sleep(0.005)

        data = "Hello World!"
        data_length = len(data)

        data_socket = create_data_socket()
        data_socket.connect((server_host, data_port))
        data_socket.send(str(data_length))

        #to keep second data transmission (data) from being part of first (data_length)
        sleep(0.005)

        send_data(data, data_socket)
        data_socket.close()
    connection_socket.close()


def create_connection_socket():
    connection_socket = socket(AF_INET, SOCK_STREAM)
    connection_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # two parentheses due to connect() only accepting one argument and requiring a tuple
    connection_socket.connect((server_host, connection_port))
    return connection_socket


def get_input():
    print "FTP>"
    ftp_input = raw_input()
    ftp_input = ftp_input.split()
    return ftp_input


def len_one_input(ftp_input):
    quit_loop = False
    if ftp_input[0] == "ls":
        ls()
    elif ftp_input[0] == "quit":
        quit_loop = True
    return quit_loop


def len_two_input(ftp_input):
    if ftp_input[0] == "get":
        get(ftp_input[1])

    elif ftp_input[0] == "put":
        put(ftp_input[1])
    else:
        print ftp_input[0] + "is not a recognized command"


def create_data_socket():
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return data_socket


def send_data(data, data_socket):
    data_sent = 0
    while data_sent != len(data):
        data_sent += data_socket.send(data[data_sent])


def ls():
    print "ls"


def get(filename):
    print filename


def put(filename):
    print filename


if __name__ == '__main__':
    main()