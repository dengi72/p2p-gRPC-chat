import resources.chat_pb2 as chat
import resources.chat_pb2_grpc as rpc
from time import sleep


class ChatServer(rpc.ServerServicer):

    def __init__(self):
        """Initialize a chat content as a list of messages."""
        self.chats = []

    def ChatStream(self, request_iterator, context):
        """Return a last message index."""
        lastindex = 0
        delay = 0.5
        while True:
            while len(self.chats) > lastindex:
                delay = 0.5
                n = self.chats[lastindex]
                lastindex += 1
                yield n
            delay = min(delay * 2, 16)
            sleep(delay)
            

    def SendNote(self, request: chat.MyMessage, context):
        """Handle a sent message."""
        self.chats.append(request)
        return chat.MyEmptyMessage()
