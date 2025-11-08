# This script invokes a predefined testcase for the object store. The test will perform different operations on the object store, increasing the workload on it. It also makes note of any errors it encounters.
# Definition of error margin: The percentage (%) of operations performed that resulted in an error.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt
import subprocess
def stress_object_store():
    initialize_empty_txt()
    print("Select your yml file below")
    print("1. test.yml")
    print("2. stress_test.yml\n")
    input2 = input("Enter your choice here: ")

    if input2 == "1":
        file = "test.yml"
    elif input2 == "2":
        file = "stress_test.yml"
    else:
        print("Invalid choice. Exiting.")
        exit()

    path = os.path.join(os.getcwd(), "MinIO", file)

    command = [
        "warp",
        "run",
        os.path.relpath(path)
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        print("/----- OBJECT STORE -----\\")
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