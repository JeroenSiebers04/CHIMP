# This script invokes a predefined testcase for the object store. The test will perform different operations on the object store, increasing the workload on it. It also makes note of any errors it encounters.
# Definition of error margin: The percentage (%) of operations performed that resulted in an error.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt
import subprocess
def stress_object_store():
    initialize_empty_txt()
    input = "2"

    if input == "1":
        file = "test.yml"
    elif input == "2":
        file = "stress_test.yml"
    else:
        print("Invalid choice. Exiting.")
        exit()

    current_path = os.path.join(__file__)
    trimmed_path = current_path.replace("\stress_object_store.py", "")
    path_string = trimmed_path + "\stress_test.yml"
    path = os.path.join(path_string)
    

    command = [
        "warp",
        "run",
        os.path.relpath(path)
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        # print("/----- OBJECT STORE -----\\")
        write_file("/----- OBJECT STORE -----\\")
        print("Command executed successfully. Output:")
        print(output)
        write_file(str(output))
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")
        write_file(f"An error occurred while trying to stress test the object store using warp: {e}")
        print(f"Error output: {e.stderr}")
        write_file(f"Error output: {e.stderr}")

if __name__ == "__main__":
    stress_object_store()