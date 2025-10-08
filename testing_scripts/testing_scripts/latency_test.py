iplist = {"http://localhost:5253", "http://localhost:5254"}

import timeit
import requests

for ip in iplist:
    ip = ip + "/ping"
    
    try:
        latency_seconds = timeit.timeit(lambda: requests.get(ip), number=1)
        response = requests.get(ip)
    
    except Exception as e:
        print(f"Could not connect to {ip}: {e}\n")
        continue

    latency_ms = latency_seconds * 1000
    if response.text != "pong":
        print(f"Unexpected response from {ip}: {response.text}\n")
    else:
        print(f"Valid response from {ip}")
        print(f"Latency of {ip}: {latency_ms:.2f} ms")