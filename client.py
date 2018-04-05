from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep
import os
connection_port = 1025
data_port = 1024
server_host = "localhost"
# Path to file location below. Change to suit your needs (Not used in current version).
path = "C:/Python27/Files"


def main():
    connection_socket = create_connection_socket()
    print("Past connection made")
    quit_loop = False
    sleep(0.005)
    while not quit_loop:
        print "FTP>"
        ftp_input = raw_input()
        ftp_input = ftp_input.split()

        if len(ftp_input) == 1:
            quit_loop = len_one_input(ftp_input, connection_socket)

        elif len(ftp_input) == 2:
            len_two_input(ftp_input, connection_socket)

        else:
            print "Unrecognized set of commands"

        # to give connection_socket time to connect
        sleep(0.005)

        # data = "Hello World!"
        # data_length = len(data)
        #
        # data_socket = create_data_socket()
        # data_socket.send(str(data_length))

        # to keep second data transmission (data) from being part of first (data_length)
        sleep(0.005)

        # send_data(data, data_socket)
        #
        # data_socket.close()
    connection_socket.close()


def create_connection_socket():
    connection_socket = socket(AF_INET, SOCK_STREAM)
    print("Part 1 of creation complete")
    connection_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print("Part 2 of creation complete")
    # two parentheses due to connect() only accepting one argument and requiring a tuple
    connection_socket.connect((server_host, connection_port))
    print("Part 3 of completion complete")
    return connection_socket


# If we have to check the directory of the server, then leave connection socket as a part of function below.
# Otherwise, remove.
def len_one_input(ftp_input, connection_socket):
    quit_loop = False
    if ftp_input[0] == "":
        print "No Command Given"
    elif ftp_input[0] == "ls":
        ls()
	connection_socket.send("ls")
    elif ftp_input[0] == "quit":
        quit_loop = True
    elif ftp_input[0] == "get":
	print "Need filename when using \"get\""
    elif ftp_input[0] == "put":
	print "Need filename when using \"put\""
    else:
        print ftp_input[0] + " Is not a recognized command"
    return quit_loop


def len_two_input(ftp_input, connection_socket):
    if ftp_input[0] == "get":
	
        connection_socket.send("get" + " " + ftp_input[1]) # Might be better to do ftp_input[0] + " " + ftp_input[1]
	
        get(ftp_input[1])

    elif ftp_input[0] == "put":
        print("in put")
        connection_socket.send("put" + " " + ftp_input[1])
        put(ftp_input[1])
    else:
        print ftp_input[0] + "is not a recognized command"

# Create socket for data to be transferred
def create_data_socket():
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    data_socket.connect((server_host, data_port))
    return data_socket


def send_data(data, socket): # By keeping track of the amount of data sent, slowly send over data.
    data_sent = 0
    print("in send_data")
    while data_sent != len(data):
        data_sent += socket.send(data[data_sent])


# List directory of the client file. Could be fixed for a different directory?
# Does it have to display the client directory? Or the server's?
def ls():
    print ("Client Directory:")
    dirs = os.listdir(os.curdir)

    for file in dirs:
        print file



# Get file of filename from the server.
def get(filename):
    print filename
    data_socket = create_data_socket()
    data_length = receive_data_length(data_socket)
  
    data = receive_data(data_socket, data_length)
    
    write_file(data, filename)


# Put file of name filename onto the server's directory.
def put(filename):
    print filename
    tmpbuffer = ""
    data = ""

    # file_size = os.path.getsize(path + "/" + filename), this code didn't work as intended
    file_size = os.stat(filename)
    data_socket = create_data_socket()
    #  the length of data to be sent over
    data_socket.send(str(file_size.st_size))
    # Open file for reading after sending the size of data through the data connection
    f = open(filename, "r")
    tmpbuffer = f.readline()

    while tmpbuffer: # While there is still information in the file, continue to iterate more and more data.
        data += tmpbuffer
        tmpbuffer = f.readline()
    sleep(0.005)
    send_data(data, data_socket)
    sleep(0.005)


# Receive length of data
def receive_data_length(socket):
    data_length = ""
    data_length += socket.recv(255)
    # data_length = int(data_length)
    return data_length


# Receive data until there is no more data to receive.
def receive_data(socket, data_length):
    print("in receive_data")
    tmpbuffer = ""
    data = ""
    print(data_length)
    while len(data) < float(data_length):
        print("receiving")
        tmpbuffer = socket.recv(30000)
        data += tmpbuffer
    print("Returning data")
    return data


def write_file(data, filename):
    f = open("test2.txt", "w+")
    f.write(data)
    f.close()


if __name__ == '__main__':
    main()
