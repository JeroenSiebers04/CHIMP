# To be continued

import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def measure_throughput_producer(queue_name, duration_sec=10):
    start_time = time.time()
    messages_sent = 0

    while True:
        # Simulating message production
        r.rpush(queue_name, "message")
        messages_sent += 1
        
        # Stop measuring after the specified duration
        if time.time() - start_time > duration_sec:
            break

    throughput = messages_sent / duration_sec
    print(f"Messages sent: {messages_sent} over {duration_sec} seconds")
    print(f"Throughput: {throughput} messages per second")

# Example usage
measure_throughput_producer(queue_name="alibaba", duration_sec=10)

connection = redis.Redis(host='localhost', port=6379, db=0)

def message_queue_throughput(queue_name):
    start_time = time.time()
    amount = 0

    while True:
        connection.rpush()