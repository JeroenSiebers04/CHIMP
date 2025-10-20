import requests

i = 0

while(i < 100):
    url = "http://localhost:5253/tasks/run/Emotion+Recognition"

    params = {
        "experiment_name": "onnx_emo_datastore",
        "user_id" : "maarten",
        "trainnew": "False",
        "basedata": "False",
        "newdata": "False",
        "personaldata": "True"
    }

    response = requests.post(url, params=params)

    print("Status code: ", response.status_code)
    print(response.text)

    i += 1

    print(f"Sent request no. {i}\n")