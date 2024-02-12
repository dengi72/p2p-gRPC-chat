import argparse
from concurrent import futures
import grpc

import resources.chat_pb2_grpc as rpc
from tkinter import *
from tkinter import simpledialog
from client import Client
from server import ChatServer


def start_client():
    """Identify a server location, then connect and start the client UI."""
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    address = None
    while address is None:
        address = simpledialog.askstring("Address", "Write server ip address", parent=root)
    root.deiconify()
    port = None
    while port is None:
        port = simpledialog.askstring("Port", "Write number of port", parent=root)
    root.deiconify()
    username = None
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    Client(username, frame, address, port)


def start_server(address, port):
    """Initialize a socket listener, then start the server UI."""
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    rpc.add_ServerServicer_to_server(ChatServer(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    print(f'Starting server on IP {address}:{port}')

    username = None
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    Client(username, frame, address, port)


def main():
    """Parse command line arguments, then run an appropriate mode."""
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-t", "--type", default="client", help="client or server")
    argument_parser.add_argument("--address", default="localhost")
    argument_parser.add_argument("--port", default=8080)

    program_args = argument_parser.parse_args()
    address = program_args.address
    port = program_args.port
    app_type = program_args.type
    if app_type == "client":
        start_client()
    elif app_type == "server":
        start_server(address, port)
    else:
        raise ValueError("type must be client or server")


if __name__ == '__main__':
    main()
