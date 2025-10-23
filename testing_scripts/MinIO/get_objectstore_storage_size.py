# This script retrieves statistics for the object store, such as storage capacity.
# Definition of storage: The amount of storage capacity used by the object store, expressed as a percentage (%) of its total capacity or as common units, such as gigabytes.

import os
import subprocess
def get_objectstore_storage_size():
    is_first_time = input("Do you want to perform intialisation? This step is required for the first use. (y/n): ")

    current_path = os.path.join(__file__)
    trimmed_path = current_path.replace("\MinIO\get_objectstore_storage_size.py", "")
    path_string = trimmed_path + "\mc.exe"
    mc = os.path.join(path_string)

    is_first_time = is_first_time.lower
    if(is_first_time != "y"):
        subprocess.run(f"{mc} admin info play")

    else:
        subprocess.run(f"{mc} alias set MyMinio http://localhost:9000 minioadmin minioadmin")

if __name__ == "__main__":
    get_objectstore_storage_size()
