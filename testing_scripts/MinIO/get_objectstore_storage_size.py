# This script retrieves statistics for the object store, such as storage capacity.
# Definition of storage: The amount of storage capacity used by the object store, expressed as a percentage (%) of its total capacity or as common units, such as gigabytes.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import subprocess
def get_objectstore_storage_size(is_first_time):
    initialize_empty_txt()
    # is_first_time should be a string, where 'y' signifies a first time usage that would require initialisation

    current_path = os.path.join(__file__)
    trimmed_path = current_path.replace("\MinIO\get_objectstore_storage_size.py", "")
    path_string = trimmed_path + "\mc.exe"
    mc = os.path.join(path_string)

    is_first_time = is_first_time.lower
    if(is_first_time != "y"):
        result = subprocess.run(f"{mc} admin info MyMinio", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_clean = result.stdout.decode('utf-8')
        print("/----- OBJECT STORE -----\\")
        write_file("\n/----- OBJECT STORE -----\\")
        print(f"\n{result_clean}")
        write_file(f"\n{result_clean}")

    else:
        subprocess.run(f"{mc} alias set MyMinio http://localhost:9000 minioadmin minioadmin")

if __name__ == "__main__":
    get_objectstore_storage_size(is_first_time='n')
