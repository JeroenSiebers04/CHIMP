# This script uses docker stats to check the current hardware usage of each docker container.
# Definition of hardware usage: The hardware that is currently being utilised by the container, expressed as a percentage (%) of the total hardware capacity.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import subprocess
def get_docker_hardware_stats(container_name):
    initialize_empty_txt()
    result = subprocess.run(f"docker stats {container_name} --no-stream", capture_output=True, text=True)

    output = result.stdout

    print("/----- DOCKER HARDWARE STATS -----\\")
    write_file("\n/----- DOCKER HARDWARE STATS -----\\\n")
    print(output)
    write_file(output)

if __name__ == "__main__":
    get_docker_hardware_stats(container_name="")