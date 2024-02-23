Group Messaging Server

This Python code implements a group messaging server using ZeroMQ (ZMQ) for real-time communication between users within a group. The server allows users to join, leave the group, send messages, and retrieve past messages.

Dependencies:
- zmq (ZeroMQ)
- threading
- datetime
- json
- uuid
- socket
- port (port.py)
- test (test.py)

Usage:
1. Ensure that the necessary dependencies are installed.
2. Run the server script.
3. Enter the group name when prompted.
4. Provide the address of the message server when prompted.
5. The server listens for incoming messages and manages user interactions.

Key Features:
- Handles JOIN requests: Users can join the group by sending a JOIN request.
- Handles LEAVE requests: Users can leave the group by sending a LEAVE request.
- Handles GET_MESSAGES requests: Users can retrieve past messages from the group.
- Handles SEND_MESSAGE requests: Users can send messages to the group.
- Messages are timestamped and stored for future retrieval.
- Provides real-time communication capabilities within the group.
- Supports concurrent access using threading and mutex locks.
- Gracefully shuts down using KeyboardInterrupt.


Message App Server

This Python script implements a message app server using ZeroMQ (ZMQ) for handling group registration and retrieving the list of active groups. The server listens for incoming requests from clients, processes them accordingly, and responds appropriately.

Dependencies:
- zmq (ZeroMQ)
- threading
- json
- socket
- test (test.py)

Usage:
1. Ensure that the necessary dependencies are installed.
2. Run the server script.
3. The server will start listening for incoming requests.
4. Clients can connect to the server to register groups and retrieve the list of active groups.

Key Features:
- Handles group registration requests from clients.
- Registers groups with unique IDs and IP addresses.
- Supports retrieval of the list of active groups.
- Provides real-time communication capabilities for managing groups.
- Supports concurrent access using threading and mutex locks.
- Gracefully handles errors and exceptions.
- Logs debug information for troubleshooting and monitoring.

Note: This server script is part of a larger messaging application system and works in conjunction with client scripts for group management and messaging.


Message App User

This Python script implements a user interface for interacting with a messaging application server. Users can perform various actions such as listing available groups, joining/leaving groups, retrieving messages from groups, and sending messages to groups.

Dependencies:
- zmq (ZeroMQ)
- uuid
- json

Usage:
1. Ensure that the necessary dependencies are installed.
2. Run the user script.
3. Follow the prompts to interact with the messaging application server.
4. Choose from options to list groups, join/leave groups, retrieve messages, or send messages.

Key Features:
- Provides a user-friendly interface for interacting with the messaging application server.
- Supports joining/leaving groups and sending/receiving messages within groups.
- Retrieves a list of available groups from the server.
- Allows users to filter messages based on a specified date.
- Handles errors and exceptions gracefully.
- Implements communication with the message application server using ZeroMQ sockets.
