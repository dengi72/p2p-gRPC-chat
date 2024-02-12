import threading

from datetime import datetime
from tkinter import *

import grpc

import resources.chat_pb2 as chat
import resources.chat_pb2_grpc as rpc


class Client:
    """Representation of user interface."""

    def __init__(self, u: str, window, address, port):
        """Creates a window in a separate thread."""
        self.window = window
        self.username = u
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ServerStub(channel)
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """Format messages recieved, than insert it into the chat."""
        for note in self.conn.ChatStream(chat.MyEmptyMessage()):
            self.chat_list.insert(END, "{}[{}]: {}\n".format(note.name, datetime.now().strftime('%H:%M:%S'),
                                                             note.message))

    def send_message(self, event):
        """Extract a message from the input bar, then send it to a reciever."""
        message = self.entry_message.get()
        if message != '':
            n = chat.MyMessage()
            n.name = self.username
            n.message = message
            self.conn.SendNote(n)
            self.entry_message.delete(0, 'end')

    def __setup_ui(self):
        """Settings used for a window output."""
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)