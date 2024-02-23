import json
import pika
import sys

class Youtuber:
    def __init__(self, name):
        self.name = name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.youtuber_requests_queue = 'youtuber_requests'
        self.channel.queue_declare(queue=self.youtuber_requests_queue)

    def publish_video(self, video_name):
        message = json.dumps({
            "name": self.name,
            "video_name": video_name
        })

        self.channel.basic_publish(exchange='', routing_key=self.youtuber_requests_queue, body=message)
        print(f"Published video: {video_name}")

        self.connection.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)
    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])
    youtuber = Youtuber(youtuber_name)
    youtuber.publish_video(video_name)
    print("SUCCESS")
