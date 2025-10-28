# This script uses the health endpoints to check if the API are available.
# Definition of availability: The endpoint is able to be reached. (It should not time out or return a NotFound.)

import requests

def get_serving_api_availability():
    ip = "http://localhost:5254/ping"

    try:
        response = requests.get(ip)
    
    except Exception as e:
        print(f"Could not connect to serving API at {ip}: {e}\n")

    print("/----- SERVING API -----\\")
    if response.text != "pong":
        print(f"Unexpected response from serving API at {ip}: {response.text}\n")
    else:
        if response.status_code == 200:
            print(f"The serving is available at {ip}. Returned http-code is as expected: {response.status_code}\n")
        else:
            print(f"Got an unexpected http-code from {ip}. Status code should be 200, but is {response.status_code}\n")
if __name__ == "__main__":
    get_serving_api_availability()