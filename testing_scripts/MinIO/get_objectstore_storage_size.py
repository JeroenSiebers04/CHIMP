import os
import subprocess

isFirstTime = input("Do you want to perform intialisation? This step is required for the first use. (y/n)")

isFirstTIme = isFirstTime.lower
if(isFirstTime != "y"):
    input = input("Please enter the file path to mc.exe (example: C:/Users/John/Desktop/mc.exe): \n")
    input = input.replace('"', '')
    path = os.path.join(input)
    subprocess.run(f"{input} admin info play")

else:
    input = input("Please enter the file path to mc.exe (example: C:/Users/John/Desktop/mc.exe): \n")
    input = input.replace('"', '')
    path = os.path.join(input)
    output = subprocess.run(f"{input} alias set MyMinio http://localhost:9000 minioadmin minioadmin")
