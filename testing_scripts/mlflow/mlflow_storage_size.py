# This scripts checks two default storage locations for MlFlow, its artifacts and its SQLite database, to determine the storage capacity used by it.
# Definition of storage capacity: The amount of storage capacity used by MlFlow, expressed in common units such as megabytes.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import subprocess
import re
def get_mlflow_storage_size():
    initialize_empty_txt()
    with open("output.txt", "w") as output_file:
        subprocess.run("docker exec mlflow-tracking-server du -sh /data/mlruns", shell=True, stdout=output_file)
        subprocess.run("docker exec mlflow-tracking-server du -sh /data/mlflow.db", shell=True, stdout=output_file)

    def convert_to_mb(size, unit):
        if unit == "M":
            return float(size)
        elif unit == "K":
            return float(size) / 1024
        elif unit == "G":
            return float(size) * 1024
        else:
            return float(size) / 1024 / 1024

    with open("output.txt", "r") as file:
        lines = file.readlines()

    total_size_mb = 0

    for line in lines:
        match = re.match(r"(\d+)([KMG]?)\s+(.+)", line.strip())
        if match:
            size = match.group(1) 
            unit = match.group(2) 
            total_size_mb += convert_to_mb(size, unit)

    print("/----- MLFLOW -----\\")
    write_file("/\n----- MLFLOW -----\\")
    print(f"Total file size used by mlflow: {total_size_mb:.2f} MB")
    write_file(f"\nTotal size file size used by mlflow: {total_size_mb:.2f} MB")

if __name__ == "__main__":
    get_mlflow_storage_size()