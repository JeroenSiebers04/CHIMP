# This script bundles all the other scripts in this folder.

keeps_going = True
while keeps_going == True:
    print("Welcome, what test would you like to perform?")
    print("[1] Test CHIMP as a whole")
    print("[2] Test separate component(s)")
    test_type = input("Please enter your choice: ")

    if test_type == "1":
        print("haha")
        keeps_going = False

    elif test_type == "2":
            print("\nList of available components to test:")
            print("[1] Training worker")
            print("[2] Serving API")
            print("[3] Training API")
            print("[4] Front End")
            print("[5] Object Store")
            print("[6] Message Queue")
            print("[7] MlFlow")
            print("\n Enter your choice as follows: 1 2 3 5 (separate values with spaces in between)")
            selected_components = input("Please enter your  choice: ")
            selected_components = selected_components.split()
            print('\n------------------------------------------------\n')
            for i in range(len(selected_components)):
                if selected_components[i] not in ['1', '2', '3', '4', '5', '6', '7']:
                    print("\nInvalid input, please try again.\n")
                else:
                    if selected_components[i] == '1':
                         print('Zet hier de training worker dingen')
                         print('\n------------------------------------------------\n')
                    if selected_components[i] == '2':
                         from API.api_availability import get_serving_api_availability
                         from API.latency_serving_api_endpoints import test_latency_serving_api_endpoints
                         get_serving_api_availability()
                         test_latency_serving_api_endpoints()
                         print('\n------------------------------------------------\n')
                    if selected_components[i] == '3':
                         from API.api_availability import get_training_api_availability
                         from API.latency_training_api_endpoint import test_latency_training_api_endpoint
                         get_training_api_availability()
                         test_latency_training_api_endpoint()
                         print('\n------------------------------------------------\n')
                    if selected_components[i] == '4':
                         print('Zet hier de frontend dingen')
                         print('\n------------------------------------------------\n')
                    if selected_components[i] == '5':
                         from MinIO.get_objectstore_storage_size import get_objectstore_storage_size
                         from MinIO.stress_object_store import stress_object_store
                         get_objectstore_storage_size()
                         #stress_object_store()
                         print('\n------------------------------------------------\n')
                    if selected_components[i] == '6':
                         print('Zet hier de message queue dingen')
                         print('\n------------------------------------------------\n')
                    if selected_components[i] == '7':
                         from MLFlow.get_mlflow_storage_size import get_mlflow_storage_size
                         get_mlflow_storage_size()
                         print('\n------------------------------------------------\n')
                    keeps_going = False
            from hardware_usage.get_docker_hardware_stats import get_docker_hardware_stats
            get_docker_hardware_stats()
            print('\n------------------------------------------------\n')

    else:
        print("\nInvalid input, please try again.\n")
        