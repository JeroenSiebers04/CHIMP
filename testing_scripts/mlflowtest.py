import mlflow
#mlflow.set_tracking_uri(uri="http://localhost:8999/")

# Create a new MLflow Experiment
#mlflow.set_experiment("MLflow Quickstart")

iplist = {"http://localhost:8999"}

import timeit
import requests


for ip in iplist:
    ip = ip 
    
    try:
        latency_seconds = timeit.timeit(lambda: requests.get(ip), number=1)
        response = requests.get(ip)
    
    except Exception as e:
        print(f"Could not connect to {ip}: {e}\n")
        continue

    latency_ms = latency_seconds * 1000
    
    
    print(f"Valid response from {ip}")
    print(f"Latency of {ip}: {latency_ms:.2f} ms")