import zmq
import threading
import datetime
import json
import uuid
import socket
from port import *
import time
from test import *

mutex=threading.Lock()
class Group:
    def __init__(self, name):
        self.uuid=str(uuid.uuid1())
        self.name = name
        self.hostname=socket.gethostname()
        self.sock_addr=socket.gethostbyname(self.hostname)
        self.port=get_new_port()
        self.context = zmq.Context()
       
        self.socket = self.context.socket(zmq.REP)
          # Assuming port 7000 for this example, you can use a different port
        self.users = []  # List to store active user IDs
        self.messages = []  # List to store sent messages with timestamps
        self.socket_1=self.context.socket(zmq.REQ)
        self.is_registered_with_message_server=False
        self.ip_address="tcp://{0}:{1}".format(self.sock_addr, self.port)
    def setup(self,ipaddress_to_message):
        hello="tcp://{0}:{1}".format(ipaddress_to_message, 5555)
        public_addr=get_ipadrress()
        pu_addr="tcp://{0}:{1}".format(public_addr, self.port)
        self.socket_1.connect(hello)
        request_data = {
            'request_type': 'register_group', 
            'arguments': {
                'group_uuid':self.uuid,
                'group_id': self.name,
                'group_name': self.name,
                'ip_address': pu_addr
            }
        }
        self.socket_1.send_string(json.dumps(request_data))  # Sending the JSON data directly
        response = self.socket_1.recv_string()
        response_json = json.loads(response)  # Parse the response as JSON

        print(f"REGISTERED WITH {hello}: {response_json['response']}")  # Access 'response' key in the parsed JSON
        self.is_registered_with_message_server=True
    def turn_up(self):
        self.socket.setsockopt(zmq.SNDTIMEO,1000)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.bind(self.ip_address)
        
        
    def start(self):
        while True:
            with mutex:
                try:
                    msg = self.socket.recv_string()
                except zmq.error.Again:
                    continue
                print("*"*20)
                if msg.startswith("JOIN"):
                    user_id = msg.split()[1]  # Extract user ID
                    print(f"JOIN REQUEST from {user_id} ")
                    if user_id not in self.users:
                        self.users.append(user_id)  # Add user to the group
                    self.socket.send_string("SUCCESS")

                elif msg.startswith("LEAVE"):
                    user_id = msg.split()[1]  # Extract user ID
                    print(f"LEAVE REQUEST from {user_id} ")
                    if user_id in self.users:
                        self.users.remove(user_id)  # Remove user from the group
                    self.socket.send_string("SUCCESS")

                elif msg.startswith("GET_MESSAGES"):
                    requested_time = None
                    print(f"GET MESSAGES REQUEST from {msg.split(',')[1]}")
                    if len(msg.split()) > 1:
                        requested_time = msg.split(",")[1]  # Extract requested time
                    messages_to_send = self.get_messages(requested_time)
                    self.socket.send_string(messages_to_send)

                elif msg.startswith("SEND_MESSAGE"):
                    print(f"SEND MESSAGES REQUEST from {msg.split(',')[1]}")
                    message_content = msg.split(",")[2]  # Extract message content
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    self.messages.append((timestamp, message_content))  # Store the message with timestamp
                    self.socket.send_string("SUCCESS")

    def get_messages(self, requested_time):
        if requested_time:
            requested_time = datetime.datetime.strptime(requested_time, '%H:%M:%S')
            selected_messages = [
                f"{msg[0]}: {msg[1]}" for msg in self.messages if datetime.datetime.strptime(msg[0], '%H:%M:%S') >= requested_time
            ]
        else:
            selected_messages = [f"{msg[0]}: {msg[1]}" for msg in self.messages]
        return "\n".join(selected_messages)
    
        
if __name__ == "__main__":
    
    group_name = input("Enter the group name: ")

    group = Group(group_name)
    ipaddress_of_server=input("Enter Message Server Address: ")

    group.setup(ipaddress_of_server)
    while not group.is_registered_with_message_server:
        time.sleep(1)
    group.turn_up()
    group.start()
    