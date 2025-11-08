# This script measures the throughput of API requests generated from the machine it is being run on. IMPORTANT --> This does not measure the total throughput experienced by the API.
# Definition of throughput: The amount of requests handled by the API per second.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import requests
import timeit

def send_requests_to_model_endpoint(amount):
    list_models_ip = "http://localhost:5253/datasets"

    i=0

    while i < amount:
        i+=1
        requests.get(list_models_ip)

def test_serving_api_throughput(amount):
    initialize_empty_txt()
    list_models_time = timeit.timeit(lambda: send_requests_to_model_endpoint(amount), number=1)
    list_models_throughput = float(amount) / list_models_time
    print("/----- TRAINING API -----\\")
    write_file("\n/----- TRAINING API -----\\")
    print(f"\nThroughput of the endpoint that lists all available datasets: {list_models_throughput:.2f} requests per second. (Using the available hardware and 1 thread)")
    write_file(f"\nThroughput of the endpoint that lists all available datasets: {list_models_throughput:.2f} requests per second. (Using the available hardware and 1 thread)")


if __name__ == "__main__":
  amount = 100
  test_serving_api_throughput(amount)