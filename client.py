from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep

connection_port = 1025
data_port = 1024
server_host = ''


def main():
    quit_loop = False
    while not quit_loop:

        print "FTP>"
        ftp_input = raw_input()
        ftp_input = ftp_input.split()

        if len(ftp_input) == 1:
            if ftp_input[0] == "ls":
                    ls()
            elif ftp_input[0] == "quit":
                    quit_loop = True

        elif len(ftp_input) == 2:
            if ftp_input[0] == "get":
                get(ftp_input[1])

            elif ftp_input[0] == "put":
                put(ftp_input[1])
            else:
                print ftp_input[0] + "is not a recognized command"

        else:
            print "Unrecognized set of commands"

        connection_socket = socket(AF_INET, SOCK_STREAM)
        connection_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # two parentheses due to connect() only accepting one argument and requiring a tuple
        connection_socket.connect((server_host, connection_port))

        #to give connection_socket time to connect
        sleep(0.005)

        data = "Hello World!"
        data_length = len(data)

        data_socket = socket(AF_INET, SOCK_STREAM)
        data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        data_socket.connect((server_host, data_port))
        data_socket.send(str(data_length))

        #to keep second data transmission (data) from being part of first (data_length)
        sleep(0.005)

        data_sent = 0

        while data_sent != len(data):
            data_sent += data_socket.send(data[data_sent])

        data_socket.close()
        connection_socket.close()


def ls():
    print "ls"


def get(filename):
    print filename


def put(filename):
    print filename


if __name__ == '__main__':
    main()