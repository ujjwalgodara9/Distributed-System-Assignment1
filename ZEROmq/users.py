import zmq
import uuid
import json
class User:
    def __init__(self):
        self.id = str(uuid.uuid1())
        print(f"User ID: {self.id}")
        self.context = zmq.Context()
        self.group_sockets = {}  # Dictionary to store group sockets
        self.server_socket_1=self.context.socket(zmq.REQ)
        self.server_socket = self.context.socket(zmq.REQ)
        self.messageserver=input("Enter Message App Address: ")
        self.hello="tcp://{0}:{1}".format(self.messageserver, 5555)
        self.server_socket.connect(self.hello)

    def get_group_list(self):
        # self.server_socket_1.connect("tcp://localhost:5555")
        request_data = {'request_type': 'get_group_list', 'origin': f"LOCALHOST:{self.id}"}
        self.server_socket.send_string(json.dumps(request_data))
        group_list_response = self.server_socket.recv_string()
        group_list = json.loads(group_list_response)['response']
        # print(group_list)
        print(f"Server list received from the message server:")
        for server in group_list:
            print(f"ServerName: {server['group_name']} - {server['ip_address']}")

    def join_group(self, group_name, group_ip):
        group_socket = self.context.socket(zmq.REQ)
        group_socket.connect(group_ip)
        group_socket.send_string(f"JOIN {str(self.id)}")
        response = group_socket.recv_string()
        if response == "SUCCESS":
            self.group_sockets[group_name] = group_socket
            print(f"Joined group '{group_name}' successfully.")
        else:
            print("Failed to join the group.")

    def leave_group(self, group_name):
        if group_name in self.group_sockets:
            group_socket = self.group_sockets[group_name]
            group_socket.send_string(f"LEAVE {str(self.id)}")
            response = group_socket.recv_string()
            if response == "SUCCESS":
                del self.group_sockets[group_name]
                print(f"Left the group '{group_name}' successfully.")
            else:
                print("Failed to leave the group.")
        else:
            print(f"You are not part of the group '{group_name}'.")

    def get_messages(self, group_name, date_filter=""):
        if group_name in self.group_sockets:
            group_socket = self.group_sockets[group_name]
            group_socket.send_string(f"GET_MESSAGES,{self.id},{date_filter}")
            messages = group_socket.recv_string()
            print(messages)
        else:
            print(f"You are not part of the group '{group_name}'.")

    def send_message(self, group_name, msg):
        if group_name in self.group_sockets:
            group_socket = self.group_sockets[group_name]
            group_socket.send_string(f"SEND_MESSAGE,{str(self.id)},{msg}")
            response = group_socket.recv_string()
            if response == "SUCCESS":
                print("Message sent successfully.")
            else:
                print("Failed to send the message.")
        else:
            print(f"You are not part of the group '{group_name}'.")

if __name__ == "__main__":
    user = User()

    while True:
        print("Select an option:")
        print("1. List groups")
        print("2. Join a group")
        print("3. Leave a group")
        print("4. Get messages from a group")
        print("5. Send message to a group")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user.get_group_list()
        elif choice == "2":
            group_name = input("Enter group name: ")
            group_ip = input("Enter group IP: ")
            user.join_group(group_name, group_ip)
        elif choice == "3":
            group_name = input("Enter group name: ")
            user.leave_group(group_name)
        elif choice == "4":
            group_name = input("Enter group name: ")
            date_filter = input("Enter date filter (optional): ")
            user.get_messages(group_name, date_filter)
        elif choice == "5":
            group_name = input("Enter group name: ")
            message = input("Enter the message: ")
            user.send_message(group_name, message)
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")