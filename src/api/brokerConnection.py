import pika
import asyncio
import time
import os
from src import ip
MY_IP = ip.get_local_ip()


RABBIT_USER = 'camera'
RABBIT_PASS = 'khargoosh'
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
rabbit_parameters = pika.ConnectionParameters(host=MY_IP,
                                              port=5672,
                                              virtual_host='wvh',
                                              credentials=credentials,
                                              connection_attempts=5,
                                              heartbeat=36000
                                              )


class BlockingRpcClient:
    def __init__(self, queue_name, recieved_topic, send_topic):
        try:
            self.connection = pika.BlockingConnection(rabbit_parameters)
            self.channel = self.connection.channel()
            self.send_topic = send_topic
            result = self.channel.queue_declare(
                queue=queue_name, exclusive=True)
            self.callback_queue = result.method.queue

            self.channel.queue_bind(
                exchange='amq.topic', queue=self.callback_queue, routing_key=recieved_topic)  # ".server.hub.12"

            self.channel.basic_consume(
                queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        except pika.exceptions.AMQPError as e:
            self.cleanup()
            raise RuntimeError(
                "Error during initialization: {}".format(str(e)))

    def on_response(self, ch, method, properties, body):
        self.response = body

    async def get_weight(self, message, timeout=5):
        try:
            self.response = None

            self.channel.basic_publish(
                exchange='amq.topic',
                routing_key=self.send_topic,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                ),
                body=message
            )
            start_time = time.time()

            while self.response is None and time.time() - start_time < timeout:
                self.connection.process_data_events()
                # A small sleep to prevent busy waiting
                await asyncio.sleep(0.01)

            print(f"=============>>>>>>{time.time()-start_time}")

            if self.response is None:
                raise TimeoutError("Timeout while waiting for response")
            return self.response

        except pika.exceptions.AMQPError as e:
            self.cleanup()
            raise RuntimeError("Error during RPC call: {}".format(str(e)))

    def close(self):
        try:
            self.connection.close()
        except pika.exceptions.AMQPError as e:
            print("Error while closing connection:", str(e))

    def cleanup(self):
        if hasattr(self, 'connection') and self.connection.is_open:
            self.connection.close()
