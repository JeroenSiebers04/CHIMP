# Write testoutput to a txt file
import os
from datetime import datetime

def write_file(result):
    current_file = os.path.join(__file__)

    file_to_write = current_file.replace("generate_test_output.py", "test_results\\test.txt")

    file_to_write = os.path.join(file_to_write)

    with open(file_to_write, "a", encoding="utf-8") as text_file:
        text_file.write(result)

def clear_file():
    current_file = os.path.join(__file__)

    file_to_write = current_file.replace("generate_test_output.py", "test_results\\test.txt")

    file_to_write = os.path.join(file_to_write)

    with open(file_to_write, "w") as text_file:
        text_file.write("")

def initialize_empty_txt():
    current_file = os.path.join(__file__)

    file_to_write = current_file.replace("generate_test_output.py", "test_results\\test.txt")

    file_to_write = os.path.join(file_to_write)

    with open(file_to_write, "r", encoding="utf-8") as text_file:
        content = []
        for line in text_file:
            content.append(line)
        if content == []:
            with open(file_to_write, "w") as text_file:
                current_datetime = datetime.now()
                text_file.write(str(current_datetime))



# This reads the output text file and prints the contents inclusing regocnition of the component that the line belongs to
if __name__ == "__main__":
    current_file = os.path.join(__file__)

    file_to_write = current_file.replace("generate_test_output.py", "test_results\\test.txt")

    file_to_write = os.path.join(file_to_write)

    with open(file_to_write, "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()

            if line.startswith("/-----") and line.endswith("-----\\"):
                current_component = line.strip("/-\\ ").strip()
                print(f"=== {current_component} ===\n")
                continue

            if line:
                if current_component:
                    print(f"[{current_component}] {line}\n")
                else:
                    print(line + "\n")