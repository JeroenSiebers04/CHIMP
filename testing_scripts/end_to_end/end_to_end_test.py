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
serving_api_throughput_finished = False

def frontend_tests():
    global frontend_tests_finished
    print("This is a placeholder for the frontend tests")
    now = time.time()
    duration = 10
    while True:
        if time.time() - now > duration:
            frontend_tests_finished = True
            break

def frontend_hardware_stress():
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_tests_finished == True:
            large_loop_iterations += 1
            print("This is a placeholder for the frontend hardware stressing")
            now = time.time()
            duration = 5
            while True:
                if time.time() - now > duration:
                    break
        else:
            time.sleep(5)

def frontend_hardware_stats():
    global frontend_hardware_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_tests_finished == True:
            large_loop_iterations += 1
            now = time.time()
            duration = 5
            i=0
            while True:
                if time.time() - now > duration:
                    break
            if i == 0:
                time.sleep(2)
                result = subprocess.run("docker stats frontend-app-abdul --no-stream", capture_output=True, text=True)
                output = result.stdout
                print("/----- DOCKER HARDWARE STATS -----\\")
                write_file("\n/----- DOCKER HARDWARE STATS -----\\\n")
                print(output)
                write_file(output)
                frontend_hardware_finished = True
        else:
            time.sleep(5)

def serving_api_availability():
    global serving_api_availability_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_hardware_finished == True:
            large_loop_iterations += 1
            from API.serving_api_availability import get_serving_api_availability
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
            time.sleep(5)

def serving_api_throughput(amount):
    global serving_api_throughput_finished
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if frontend_hardware_finished == True:
            large_loop_iterations += 1
            from API.serving_api_throughput import test_serving_api_throughput
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
            time.sleep(5)

def serving_api_hardware(amount):
    large_loop_iterations = 0
    while large_loop_iterations == 0:
        if serving_api_throughput_finished == True:
            large_loop_iterations += 1
            from hardware_usage.stress_serving_api import stress_serving_api_hardware
            print("Starting hardware stress on serving API")
            now = time.time()
            duration = 60
            small_loop_iterations = 0
            while True:
                if time.time() - now > duration:
                    print("60 seconds elapsed")
                    break
                if small_loop_iterations == 0:
                    small_loop_iterations += 1
                    stress_serving_api_hardware(amount)
                    
        else:
            time.sleep(5)

def start_end_to_end_test():
    tasks =[
        (frontend_tests, 0),
        (frontend_hardware_stress, 0),
        (frontend_hardware_stats, 0),
        (serving_api_availability, 0),
        (lambda: serving_api_throughput(amount=1000), 0),
        (lambda: serving_api_hardware(amount=50000), 0)
        #(lambda: end_to_end_test(1), 4) example of passing argument
        
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
