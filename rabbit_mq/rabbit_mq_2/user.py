import json
import pika
import sys

class User:
    def __init__(self, name):
        self.name = name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.user_requests_queue = 'user_requests'
        self.user_notifications_queue = f'user_notifications_{self.name}'
        self.channel.queue_declare(queue=self.user_requests_queue)
        self.channel.queue_declare(queue=self.user_notifications_queue)

    def update_subscription(self, youtuber_name, action):
        message = json.dumps({
            "user": self.name,
            "youtuber": youtuber_name,
            "action": action
        })

        self.channel.basic_publish(exchange='', routing_key=self.user_requests_queue, body=message)
        print("SUCCESS")

    def receive_notifications(self, ch, method, properties, body):
        print("New Notification:", body.decode())

    def start_receiving_notifications(self):
        self.channel.basic_consume(queue=self.user_notifications_queue, on_message_callback=self.receive_notifications, auto_ack=True)
        print(f"Waiting for notifications. To exit press CTRL+C")
        self.channel.start_consuming()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: User.py <UserName> [s/u YoutuberName]")
        sys.exit(1)

    user_name = sys.argv[1]
    user = User(user_name)

    if len(sys.argv) == 4 and (sys.argv[2] == 's' or sys.argv[2] == 'u'):
        action = 'subscribe' if sys.argv[2] == 's' else 'unsubscribe'
        youtuber_name = sys.argv[3]
        user.update_subscription(youtuber_name, action)
    elif len(sys.argv) == 2:
        user.start_receiving_notifications()
    else:
        print("Invalid arguments")
