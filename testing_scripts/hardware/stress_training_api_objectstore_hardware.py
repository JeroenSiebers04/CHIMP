# This script generates a workload on the training API and the object store by sending a large amount of requests for ___

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import requests
import threading

def stress_training_api_objectstore_hardware(thread_id, requests_per_thread):
    url = "http://localhost:5253/datasets"
    i = 0
    try:
        while i < requests_per_thread:
            response = requests.get(url)
            print(f"Thread {thread_id} - Status code: {response.status_code}")
            print(f"Thread {thread_id} - Response: {response.text}")
            i += 1
            print(f"Thread {thread_id} - Finished request {i} of {requests_per_thread}\n")
        print("Script finished successfully.")
        write_file("\n/----- TRAINING API -----\\")
        write_file(f"\nSuccessfully finished sending {requests_per_thread} API requests per thread to the endpoint that lists all available datasets to generate a load on the training API.")

    except Exception as e:
        print("/----- TRAINING API - ERROR REPORT -----\\")
        print(f"Thread {thread_id} - Encountered an error at request no.{i}")
        print(f"Thread {thread_id} - Error details: {str(e)}")
        if int(thread_id) == 1:
            write_file("\n/----- TRAINING API - ERROR REPORT -----\\")
            write_file(f"\nThread {thread_id} - Encountered an error when sending {requests_per_thread} API requests per thread to the endpoint that listsall available datasets to generate a load on the training API and objectstore at request no.{i}")
            write_file(f"\nThread {thread_id} - Error details: {str(e)}")

def start_stress_training_api_objectstore_hardware(threads_amount, requests_per_thread):
    initialize_empty_txt()
    threads = []
    for i in range(threads_amount):
        thread_id = i+1
        thread = threading.Thread(target=stress_training_api_objectstore_hardware, args=(thread_id, requests_per_thread))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    requests_per_thread = 1000
    threads_amount = 50
    start_stress_training_api_objectstore_hardware(threads_amount, requests_per_thread)