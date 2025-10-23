# This script generates a workload on the serving API by sending a large amount of requests for a list of all available models

import requests

def stress_serving_api_hardware(amount):
    url = "http://localhost:5254/model"
    i=0
    try:
        while i < amount:
            i += 1

            response = requests.get(url)

            print(f"Status code: {response.status_code}")
            print(response.text)
            print(f"Finished request {i} of {amount}\n")

    except Exception as e:
        print("/----- SERVING API - ERROR REPORT -----\\")
        print(f"Encountered an error at API request no. {i}")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    try:
        amount_str = input("How many API requests would you like to send to the serving API? ")
        amount = int(amount_str)
        stress_serving_api_hardware(amount)
    except:
        print("Input could not be converted to a numeric value. Please enter only a number.")