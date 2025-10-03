iplist = {"http://localhost:5252", "http://localhost:5253", "http://localhost:5254", "http://localhost:8999"}

import timeit
import requests

for ip in iplist:
    latency_seconds = timeit.timeit(lambda: requests.get(ip), number=1)

    latency_ms = latency_seconds * 1000

    print(f"Latency of {ip}: {latency_ms:.2f} ms")