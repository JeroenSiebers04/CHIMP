# This script checks the latency of an endpoint for the training API: starting a training job
# Definition of latency: The time it takes from making the request to getting a confirmation that training has been started from the endpoint.
import requests
import timeit

def test_latency_training_api_endpoint():

    print("/----- TRAINING API -----\\")

    url = "http://localhost:5253/tasks/run/Emotion+Recognition"

    params = {
        "experiment_name": "onnx_emo_datastore",
        "user_id" : "maarten",
        "trainnew": "False",
        "basedata": "False",
        "newdata": "False",
        "personaldata": "True"
    }

    latency_s = timeit.timeit(lambda: requests.post(url, params=params), number=1)
    latency_ms = latency_s * 1000
    response = requests.post(url, params=params)
    if response.status_code == 200:
        if "task started successfully" in response.text:
            print(f"Latency when starting model calibration: {latency_ms:.2f}ms. Returned http-code is as expected: {response.status_code}")
        else:
            print("Unable to determine if task was created successfully.\n")
    else:
        print(f"Got an unexpected http-code from {url}. Status code should be 200, but is {response.status_code}")
if __name__ == "__main__":
    test_latency_training_api_endpoint()