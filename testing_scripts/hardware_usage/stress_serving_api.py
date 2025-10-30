# This script generates a workload on the serving API by sending a large amount of requests for a list of all available models

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  generate_test_output import write_file, initialize_empty_txt

import requests

def stress_serving_api_hardware(amount):
    initialize_empty_txt()
    url = "http://localhost:5254/model"
    i=0
    try:
        while i < amount:
            i += 1

            response = requests.get(url)

            print(f"Status code: {response.status_code}")
            print(response.text)
            print(f"Finished request {i} of {amount}\n")

        print("Script finished successfully.")
        write_file("\n/----- SERVING API -----\\")
        write_file(f"\nSuccessfully finished sending {amount} API requests to the endpoint that lists all available models to generate a load on the serving API.")

    except Exception as e:
        print("/----- SERVING API - ERROR REPORT -----\\")
        write_file("\n/----- SERVING API - ERROR REPORT -----\\")
        print(f"Encountered an error at API request no. {i}")
        write_file(f"\nEncountered an error when sending {amount} API requests to the endpoint that lists all available models to generate a load on the serving API at API request no. {i}")
        print(f"Error details: {str(e)}")
        write_file(f"\nError details: {str(e)}")

if __name__ == "__main__":
    try:
        amount_str = input("How many API requests would you like to send to the serving API? ")
        amount = int(amount_str)
        stress_serving_api_hardware(amount)
    except:
        print("Input could not be converted to a numeric value. Please enter only a number.")