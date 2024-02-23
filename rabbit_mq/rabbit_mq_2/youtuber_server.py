import json
import pika

class YouTubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.user_requests_queue = 'user_requests'
        self.youtuber_requests_queue = 'youtuber_requests'
        self.notifications_queue = 'notifications'

        self.subscriptions = {}  # Simulating a storage for user subscriptions

        self.channel.queue_declare(queue=self.user_requests_queue)
        self.channel.queue_declare(queue=self.youtuber_requests_queue)

    def consume_user_requests(self, ch, method, properties, body):
        message = json.loads(body.decode())
        action = message['action']
        user = message['user']

        if action == 'login':
            print(f"{user} logged in")
        elif action in ['subscribe', 'unsubscribe']:
            self.update_subscription(user, message['youtuber'], action == 'subscribe')
            print(f"{user} {action}d to {message['youtuber']}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_youtuber_requests(self, ch, method, properties, body):
        message = json.loads(body.decode())
        youtuber_name = message['name']
        video_name = message['video_name']
        
        self.notify_users_of_new_video(youtuber_name, video_name)
        print(f"{youtuber_name} uploaded {video_name}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def update_subscription(self, user, youtuber_name, subscribe):
        if subscribe:
            if youtuber_name not in self.subscriptions:
                self.subscriptions[youtuber_name] = set()
            self.subscriptions[youtuber_name].add(user)
        else:
            if youtuber_name in self.subscriptions:
                self.subscriptions[youtuber_name].discard(user)

    def notify_users_of_new_video(self, youtuber_name, video_name):
        if youtuber_name in self.subscriptions:
            for user in self.subscriptions[youtuber_name]:
                self.notify_users(user, f"New Notification: {youtuber_name} uploaded {video_name}")

    def notify_users(self, user, notification):
        user_notification_queue = f'user_notifications_{user}'
        self.channel.queue_declare(queue=user_notification_queue)
        self.channel.basic_publish(exchange='', routing_key=user_notification_queue, body=notification)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.user_requests_queue, on_message_callback=self.consume_user_requests)
        self.channel.basic_consume(queue=self.youtuber_requests_queue, on_message_callback=self.consume_youtuber_requests)
        print("YouTube Server Started. Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

if __name__ == "__main__":
    youtube_server = YouTubeServer()
    youtube_server.start_consuming()
