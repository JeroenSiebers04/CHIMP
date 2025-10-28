# This script uses the health endpoints to check if the API are available.
# Definition of availability: The endpoint is able to be reached. (It should not time out or return a NotFound.)

import requests

def get_training_api_availability():
    ip = "http://localhost:5253/ping"

    try:
        response = requests.get(ip)
    
    except Exception as e:
        print(f"Could not connect to training API at {ip}: {e}\n")
    
    print("/----- TRAINING API -----\\")
    if response.text != "pong":
        print(f"Error: Unexpected response from training API at {ip}: {response.text}\n")
    else:
        if response.status_code == 200:
            print(f"The training api is available at {ip}. Returned http-code is as expected: {response.status_code}\n")
        else:
            print(f"Got an unexpected http-code from {ip}. Status code should be 200, but is {response.status_code}\n")


if __name__ == "__main__":
    get_training_api_availability()