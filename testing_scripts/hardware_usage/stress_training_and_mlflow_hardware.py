# This script utilises the API endpoint to start an amount of model calibration jobs to generate a big workload on the training worker and MlFLow and a spike in network I/O

import requests

def stress_training_and_mlflow_hardware(amount):
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

    except Exception as e:
        print("/----- TRAINING API - ERROR REPORT -----\\")
        print(f"Encountered an error at API request no. {i}")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    try:
        amount_str = input("How many API requests to start model calibration would you like to send? ")
        amount = int(amount_str)
        stress_training_and_mlflow_hardware(amount)
    except:
        print("Input could not be converted to a numeric value. Please enter only a number.")