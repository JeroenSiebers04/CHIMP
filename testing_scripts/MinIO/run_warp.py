
import os
import subprocess

print("Select your yml file below")
print("1. test.yml")
print("2. stress_test.yml\n")
input = input("Enter your choice here: ")

if input == "1":
    file = "test.yml"
elif input == "2":
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
    print("Command executed successfully. Output:")
    print(output)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing the command: {e}")
    print(f"Error output: {e.stderr}")