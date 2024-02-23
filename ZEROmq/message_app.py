import zmq
import threading
import json
import socket
from test import *
zmq_version = zmq.zmq_version_info()
major_version = zmq_version[0]
class MessageAppServer:
    def __init__(self,ipaddr):
        self.groups = {}  # Dictionary to store group details
        self.registry_socket = None
        self.context = zmq.Context()
        self.mutex = threading.Lock()
        self.binding="tcp://{0}:{1}".format(ipaddr, 5555)

    def start(self):
        self.__setup()
        print("STARTING MESSAGE APP SERVER...")
        while True:
            with self.mutex:
                try:
                    request_bytes = self.registry_socket.recv()

                    if major_version >= 4:
                        # Retrieve socket state
                        state = self.registry_socket.getsockopt(zmq.RCVMORE)
                        print(f"Socket state before receiving: {state}")

                    # Convert bytes to string
                    request_str = request_bytes.decode('utf-8')

                    # Add debug statement to inspect received data in string format
                    print(f"Received data: {request_str}")

                    if request_str:  # Check if data is not empty
                        try:
                            request = json.loads(request_str)
                            self.__handle_request(request)
                            if major_version >= 4:
                                # Retrieve socket state after processing
                                state = self.registry_socket.getsockopt(zmq.RCVMORE)
                                print(f"Socket state after receiving: {state}")
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {str(e)}")
                    else:
                        print("Received an empty request. Ignoring.")

                except zmq.Again:
                    continue
                except zmq.error.ZMQError as e:
                    print(f"ZMQError: {str(e)}")
                    # Reset the socket if needed
                    self.registry_socket.close()
                    self.__setup()

    def __setup(self):
        self.registry_socket = self.context.socket(zmq.REP)
        self.registry_socket.setsockopt(zmq.SNDTIMEO, 1000)
        self.registry_socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.registry_socket.bind(self.binding)

    def __handle_request(self, req):
        try:
            if req:
                if req['request_type'] == 'register_group':
                    print(f"REGISTER REQUEST FROM {req['arguments']['ip_address']}")
                    self.register_group(req['arguments'])
                elif req['request_type'] == 'get_group_list':
                    # Handle the GetGroupList request
                    print(f"GROUP LIST REQUEST FROM {req['origin']}")
                    self.get_group_list(req['origin'])
            else:
                print("Received an empty request. Ignoring.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")

    def register_group(self, group_info):
        group_id = group_info['group_uuid']
        if group_id not in self.groups:
            self.groups[group_id] = {
                'group_uuid':group_info['group_uuid'],
                'group_name': group_info['group_name'],
                'ip_address': group_info['ip_address']
            }
            status = 'SUCCESS'
        else:
            status = 'FAIL (Group already exists)'
        self.registry_socket.send_string(json.dumps({'request_type': 'register_group', 'response': status}))

    def get_group_list(self, user_address):
        group_list = list(self.groups.values())
        response = json.dumps({'request_type': 'get_group_list', 'response': group_list})
        self.registry_socket.send_string(response)
        print("Group list sent to the user.")

if __name__ == "__main__":
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    print(get_ipadrress())

    print("Message Server running: "+ip+':50001')
    server = MessageAppServer(ip)
    # server.setup()
    server.start()
