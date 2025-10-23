# This script checks the latency of two endpoints for the serving API: 1. retrieving a list of all models, 2. requesting inference from the model.
# Definition of latency: 1. The time it takes from making the request to receiving a list of all models, 2. The time it takes from making the request to recieving a response from the inference endpoint.

import timeit
import requests

def test_latency_serving_api_endpoints():
  print("/----- SERVING API -----\\")

  list_models_ip = "http://localhost:5254/model"

  latency_list_models_s = timeit.timeit(lambda: requests.get(list_models_ip), number=1)
  latency_list_models_ms = latency_list_models_s * 1000
  response_list_models = requests.get(list_models_ip)

  if response_list_models.status_code == 200:
    print(f"Latency when retrieving a list of all available models: {latency_list_models_ms:.2f}ms. Returned status code: {response_list_models.status_code}")
  else:
    print(f"Got an unexpected http-code from {list_models_ip}. Status code should be 200, but is {response_list_models.status_code}")

  inference_ip = "http://localhost:5254/model/onnx_emo_datastore/infer"

  mock_json_input = {
    "inputs": ["a"]
  }

  latency_inference_s = timeit.timeit(lambda: requests.post(inference_ip, json=mock_json_input), number=1)
  latency_inference_ms = latency_inference_s * 1000
  response_inference = requests.post(inference_ip, json=mock_json_input)
  
  if response_inference.status_code == 500:
    print(f"Latency when requesting inference from onnx_emo_datastore model: {latency_inference_ms:.2f}ms. Returned status code: {response_inference.status_code}")
  else:
    print(f"Got an unexpected http-code from {inference_ip}. Status code should be 500, but is {response_inference.status_code}")

if __name__ == "__main__":
  test_latency_serving_api_endpoints()