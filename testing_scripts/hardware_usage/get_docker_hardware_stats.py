# This script uses docker stats to check the current hardware usage of each docker container.
# Definition of hardware usage: The hardware that is currently being utilised by the container, expressed as a percentage (%) of the total hardware capacity.

import subprocess
def get_docker_hardware_stats():
    result = subprocess.run("docker stats --no-stream", capture_output=True, text=True)

    output = result.stdout

    print("/----- DOCKER HARDWARE STATS -----\\")
    print(output)

if __name__ == "__main__":
    get_docker_hardware_stats()