import sys
import os
import time
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generate_test_output import write_file, initialize_empty_txt
import subprocess

#placeholders of values to test

frontend_tests_finished = False
frontend_hardware_finished = False
serving_api_availability_finished = False
serving_api_latency_finished = False
serving_api_throughput_finished = False
serving_api_hardware_started = False
serving_api_hardware_finished = False
mlflow_latency_finished = False
mlflow_storage_size_finished = False
mlflow_hardware_started = False
mlflow_hardware_finished = False

frontend_tests_finished2 = False
frontend_hardware_started2 = False
frontend_hardware_finished2 = False

# End to end for the interaction where a user uses the model
def frontend_tests():
    global frontend_tests_finished
    print("This is a placeholder for the frontend tests")
    now = time.time()
    duration = 5
    i=0
    while True:
        if time.time() - now > duration:
            frontend_tests_finished = True
            break
        if i == 0:
            i += 1
            print("/----- FRONTEND -----\\")

def frontend_hardware():
    global  frontend_tests_finished
    global frontend_hardware_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_tests_finished == True:
            large_loop_iterations += 1
            print("This is a placeholder for the frontend hardware stressing")
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    print("done hardware stress")
                    break
                if i == 0:
                    i += 1
                    print("/----- FRONTEND -----\\")
                    frontend_hardware_finished = True

        else:
            time.sleep(1)

def frontend_hardware_stats():
    global frontend_hardware_finished
    global frontend_tests_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_tests_finished == True:
            large_loop_iterations += 1
            from hardware.get_docker_hardware_stats import get_docker_hardware_stats
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                i += 1
                time.sleep(2)
                get_docker_hardware_stats(container_name="frontend-app-abdul")
        else:
            time.sleep(1)

def serving_api_availability():
    global serving_api_availability_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_hardware_finished == True:
            large_loop_iterations += 1
            from serving_api.serving_api_availability import get_serving_api_availability
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
                if i == 0:
                    i += 1
                    get_serving_api_availability()
                    serving_api_availability_finished = True
        else:
            time.sleep(1)

def serving_api_latency():
    global serving_api_availability_finished
    global serving_api_latency_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if serving_api_availability_finished == True:
            large_loop_iterations += 1
            from serving_api.serving_api_latency import test_latency_serving_api_endpoints
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
                if i == 0:
                    i += 1
                    test_latency_serving_api_endpoints()
                    serving_api_latency_finished = True
        else:
            time.sleep(1)

def serving_api_throughput(amount):
    global serving_api_throughput_finished
    global serving_api_latency_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if serving_api_latency_finished == True:
            large_loop_iterations += 1
            from serving_api.serving_api_throughput import test_serving_api_throughput
            now = time.time()
            duration = 10
            i = 0
            while True:
                if time.time() - now > duration:
                    break
                if i == 0:
                    i += 1
                    test_serving_api_throughput(amount)
                    serving_api_throughput_finished = True
        else:
            time.sleep(1)

def serving_api_hardware(amount):
    global serving_api_throughput_finished
    global serving_api_hardware_started
    global serving_api_hardware_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if serving_api_throughput_finished == True:
            large_loop_iterations += 1
            from hardware.stress_serving_api import stress_serving_api_hardware
            now = time.time()
            duration = 60
            i = 0
            while True:
                if time.time() - now > duration:
                    serving_api_hardware_finished = True
                    break
                if i == 0:
                    print("Starting hardware stress on serving API")
                    i += 1
                    serving_api_hardware_started = True
                    stress_serving_api_hardware(amount)
                    
        else:
            time.sleep(1)

def serving_api_hardware_stats():
    global serving_api_hardware_started
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if serving_api_hardware_started == True:
            time.sleep(5)
            large_loop_iterations += 1
            from hardware.get_docker_hardware_stats import get_docker_hardware_stats
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                i += 1
                time.sleep(2)
                get_docker_hardware_stats(container_name="serving-api")
        else:
            time.sleep(1)

def mlflow_latency():
    global serving_api_hardware_finished
    global mlflow_latency_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if serving_api_hardware_finished == True:
            large_loop_iterations += 1
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                i += 1
                print("\n/----- MLFLOW -----\\ \nMLFlow latency placeholder")
                mlflow_latency_finished = True

        else:
            time.sleep(1)

def mlflow_storage_size():
    global mlflow_latency_finished
    global mlflow_storage_size_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if mlflow_latency_finished == True:
            large_loop_iterations += 1
            from mlflow.get_mlflow_storage_size import get_mlflow_storage_size
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                i += 1
                get_mlflow_storage_size()
                mlflow_storage_size_finished = True

        else:
            time.sleep(1)

def mlflow_hardware():
    global mlflow_hardware_finished
    global mlflow_storage_size_finished
    global mlflow_hardware_started
    large_loop_iterations = 0
    now = time.time()
    while large_loop_iterations == 0:
        if mlflow_storage_size_finished == True:
            large_loop_iterations += 1
            duration = 60
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                i += 1
                mlflow_hardware_started = True
                print("\n/----- MLFLOW -----\\ \nMLFlow hardware placeholder")
                mlflow_hardware_finished = True

        else:
            time.sleep(1)

def mlflow_hardware_stats():
    global mlflow_hardware_started
    large_loop_iterations = 0
    now = time.time()
    while large_loop_iterations == 0:
        if mlflow_hardware_started == True:
            time.sleep(5)
            large_loop_iterations += 1
            from hardware.get_docker_hardware_stats import get_docker_hardware_stats
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                i += 1
                time.sleep(2)
                get_docker_hardware_stats(container_name="mlflow-tracking-server")
        else:
            time.sleep(1)

def start_end_to_end_test():
    tasks =[
        (frontend_tests, 0),
        (frontend_hardware, 5),
        (frontend_hardware_stats, 5),
        (serving_api_availability, 10),
        (serving_api_latency, 15),
        (lambda: serving_api_throughput(amount=1000), 20),
        (lambda: serving_api_hardware(amount=50000), 25),
        (serving_api_hardware_stats, 25),
        (mlflow_latency, 85),
        (mlflow_storage_size, 90),
        (mlflow_hardware, 95),
        (mlflow_hardware_stats, 100)
    ]
    
    threads = []

    for fn, delay in tasks:
        # Wrap the function to apply the start delay
        def wrapper(f=fn, d=delay):
            time.sleep(d)
            f()

        t = threading.Thread(target=wrapper)
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("All tasks finished")

if __name__ == "__main__":
    start_end_to_end_test()
