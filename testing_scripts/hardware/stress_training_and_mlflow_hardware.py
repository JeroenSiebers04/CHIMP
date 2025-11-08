# This script utilises the API endpoint to start an amount of model calibration jobs to generate a big workload on the training worker and MlFLow and a spike in network I/O

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import requests

def stress_training_and_mlflow_hardware(amount):
    initialize_empty_txt()
    i = 0
    try:
        while(i < amount):
            url = "http://localhost:5253/tasks/run/Emotion+Recognition"

            params = {
                "experiment_name": "onnx_emo_datastore",
                "user_id" : "maarten",
                "trainnew": "False",
                "basedata": "False",
                "newdata": "False",
                "personaldata": "True"
            }

            i += 1
            response = requests.post(url, params=params)

            print("Status code: ", response.status_code)
            print(response.text)

            print(f"Sent request no. {i}\n")
        print("Script finished successfully.")
        write_file("\n/----- TRAINING API -----\\")
        write_file(f"\nSuccessfully finished sending {amount} API requests to the endpoint that creates a model calibration task to generate a load on the training worker and mlflow.")

    except Exception as e:
        print("/----- TRAINING API - ERROR REPORT -----\\")
        write_file("\n/----- TRAINING API - ERROR REPORT -----\\")
        print(f"Encountered an error when sending {amount} API requests to the endpoint that creates a model calibration task to generate a load on the training worker and mlflow at API request no. {i}")
        write_file(f"\nEncountered an error when sending {amount} API requests to the endpoint that creates a model calibration task to generate a load on the training worker and mlflow at API request no. {i}")
        print(f"Error details: {str(e)}")
        write_file(f"\nError details: {str(e)}")

if __name__ == "__main__":
    try:
        amount_str = input("How many API requests to start model calibration would you like to send? ")
        amount = int(amount_str)
        stress_training_and_mlflow_hardware(amount)
    except:
        print("Input could not be converted to a numeric value. Please enter only a number.")