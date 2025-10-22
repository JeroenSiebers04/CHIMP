# This script uses the health endpoints to check if the API are available.
# Definition of availability: The endpoint is able to be reached. (It should not time out or return a NotFound.)
import timeit
import requests
# def test_api_availability():
#     iplist = {"http://localhost:5253", "http://localhost:5254"}

#     for ip in iplist:
#         ip = ip + "/ping"
        
#         try:
#             latency_seconds = timeit.timeit(lambda: requests.get(ip), number=1)
#             response = requests.get(ip)
        
#         except Exception as e:
#             print(f"Could not connect to {ip}: {e}\n")
#             continue

#         latency_ms = latency_seconds * 1000
#         if response.text != "pong":
#             print(f"Unexpected response from {ip}: {response.text}\n")
#         else:
#             print(f"Valid response from {ip}")
#             print(f"Latency of {ip}: {latency_ms:.2f} ms")

def get_training_api_availability():
    ip = "http://localhost:5253/ping"

    try:
        latency_seconds = timeit.timeit(lambda: requests.get(ip), number=1)
        response = requests.get(ip)
    
    except Exception as e:
        print(f"Could not connect to training API at {ip}: {e}\n")

    latency_ms = latency_seconds * 1000
    if response.text != "pong":
        print(f"Unexpected response from training API at {ip}: {response.text}\n")
    else:
        print(f"Valid response from training API at {ip}. Status code: {response.status_code}")
        print(f"Latency of training API at {ip}: {latency_ms:.2f} ms")

def get_serving_api_availability():
    ip = "http://localhost:5254/ping"

    try:
        latency_seconds = timeit.timeit(lambda: requests.get(ip), number=1)
        response = requests.get(ip)
    
    except Exception as e:
        print(f"Could not connect to serving API at {ip}: {e}\n")

    latency_ms = latency_seconds * 1000
    if response.text != "pong":
        print(f"Unexpected response from serving API at {ip}: {response.text}\n")
    else:
        print(f"Valid response from serving API at {ip}. Status code: {response.status_code}")
        print(f"Latency of serving API at {ip}: {latency_ms:.2f} ms")

if __name__ == "__main__":
    get_training_api_availability()
    get_serving_api_availability()