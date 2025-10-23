# This script generates a workload on the straining API by sending a large amount of requests for ___

import requests
import threading

def stress_training_api_hardware(thread_id, requests_per_thread):
    url = "http://localhost:5253/datasets"
    i = 0
    try:
        while i < requests_per_thread:
            response = requests.get(url)
            print(f"Thread {thread_id} - Status code: {response.status_code}")
            print(f"Thread {thread_id} - Response: {response.text}")
            i += 1
            print(f"Thread {thread_id} - Finished request {i} of {requests_per_thread}\n")
    except Exception as e:
        print(f"Thread {thread_id} - Encountered an error at request no.{i}")
        print(f"Thread {thread_id} - Error details: {str(e)}")

def start_stress_training_api_hardware(threads_amount, requests_per_thread):
    threads = []
    for i in range(threads_amount):
        thread_id = i+1
        thread = threading.Thread(target=stress_training_api_hardware, args=(thread_id, requests_per_thread))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    requests_per_thread = 1000
    threads_amount = 50
    start_stress_training_api_hardware(threads_amount, requests_per_thread)