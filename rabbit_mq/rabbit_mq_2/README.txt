User Subscription Management System

This Python script implements a user interface for managing subscriptions to YouTubers. Users can subscribe or unsubscribe to YouTubers and receive notifications about new videos from subscribed YouTubers.

Dependencies:
- json
- pika (RabbitMQ Python client library)
- sys

Usage:
1. Ensure that RabbitMQ is installed and running locally.
2. Install the necessary Python dependencies.
3. Run the User.py script with appropriate arguments.

Command-line Arguments:
- `<UserName>`: Specifies the name of the user.
- `[s/u YoutuberName]`: Optional. Indicates whether the user wants to subscribe (`s`) or unsubscribe (`u`) from a YouTuber specified by `YoutuberName`.
  - Example: `User.py John s PewDiePie`
- If no additional arguments are provided, the script starts listening for notifications about new videos from subscribed YouTubers for the user.

Key Features:
- Allows users to subscribe/unsubscribe to YouTubers and receive notifications about new videos.
- Implements communication with a RabbitMQ message broker for message queuing and distribution.
- Supports command-line arguments for ease of use and flexibility.
- Provides clear usage instructions and error messages for users.
- Utilizes JSON for message serialization/deserialization.

YouTube Server

This Python script serves as a server-side application for managing subscriptions and notifying users about new videos uploaded by YouTubers. It communicates with users and YouTubers via RabbitMQ message queues.

Dependencies:
- json
- pika (RabbitMQ Python client library)

Usage:
1. Ensure that RabbitMQ is installed and running locally.
2. Install the necessary Python dependencies.
3. Run the YouTubeServer.py script.

Key Features:
- Manages user subscriptions and notifies users about new videos from subscribed YouTubers.
- Utilizes RabbitMQ for message queuing and distribution between users, YouTubers, and the server.
- Supports login, subscribe, and unsubscribe actions from users.
- Receives requests from YouTubers to notify users about new video uploads.
- Simulates a storage mechanism for user subscriptions using a dictionary.
- Provides clear console output for logging login events, subscription actions, and new video notifications.
- Implements basic error handling and acknowledgment of message delivery to ensure reliability.
- Easy to run and integrate into existing systems with minimal setup.
- Designed for scalability and extensibility, allowing for potential expansion of features and functionalities.

Youtuber

This Python script represents a YouTuber entity that publishes a new video by sending a request to the YouTube Server via RabbitMQ message queue.

Dependencies:
- json
- pika (RabbitMQ Python client library)

Usage:
1. Ensure that RabbitMQ is installed and running locally.
2. Install the necessary Python dependencies.
3. Run the Youtuber.py script with the YouTuber's name and the name of the video to be published as command-line arguments.

Key Features:
- Sends a request to the YouTube Server to publish a new video with the specified name.
- Utilizes RabbitMQ for message queuing and communication with the YouTube Server.
- Provides clear console output indicating the successful publication of the video.
- Designed for simplicity and ease of use, requiring only the YouTuber's name and the video name as input arguments.
- Supports integration with existing systems and workflows through RabbitMQ message queues.
