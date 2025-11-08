# Testtool CHIMP

This testtool is made for the CHIMP project. It aims to stress the docker containers inside the CHIMP project and measure Key Performance Indicators (KPIs) for every container that will assist in concluding whether a component is considered a bottleneck.

## Important information
Some of the scripts in this project do something that applies to multiple components. Therefore, not each KPI gets its very own script. Sometimes a KPI for a component can be determined from the data of another script. The KPI that are measured through different scripts than `<Name>_<KPI>.py` are as follows:

- **MLFlow latency**:
  The latency of MLFlow can be determined by looking at the time it took to retrieve a list of models from the serving API as this directly communicates with MLFlow to gather said list.
  
- **Object Store error rate**:
  The error rate for the object store can be determined through the program used to run its stress tests (benchmarks). The report that it generates after it finished the test contains both the total operations and the amount of errors. This leads to the error rate by performing the following calculation: `errors / total operations * 100`

- **Stress testing the Training Worker and MLFlow**:
  The script named `stress_training_and_mlflow_hardware.py` is designed to generate a spike in hardware usage for both the Training Worker and MLFlow.

- **Stress testing the Training API and the Object Store**:
  The script names `stress_training_api_obejctstore_hardware.py` is designed to generate a spike in hardware usage for both the Training API and the Object Store.

## Uses of the tool

The tool has 2 main uses: performing a specific component test on the specified container and performing an end-to-end test for the whole CHIMP project, which uses stress tests and measurements together. The webpage for this tool offers easy access to performing these tests.

## Prerequisites

- **Guide - Adding a program to PATH environment variable**:  
  [Windows] Open the search bar > Search "Edit the system environment variables" > Select "Environment Variables" > Under system variables, select `PATH`, then select "Edit" > select "New: > Enter the file path (C:\Path\To\File) to the `.exe`.

- **GO**:  
  GO is a required tool for installing the next prerequisite. It is available at: [https://go.dev/](https://go.dev/). Once GO is installed, it should be added to the PATH environment variables.

- **Warp**:  
  Warp is a MinIO benchmarking tool used to gather information about the performance of different operations performed by the object store. Warp is available for installation at: [https://github.com/minio/warp](https://github.com/minio/warp). Once Warp is installed, it should be added to the PATH environment variables.

- **Python packages**:  
  Finally, the required Python packages should be installed. This can be done by cloning this project, navigating to the `testing_scripts` folder, and performing the following command:  
  `pip install -r requirements.txt`

## Interpreting the data

When the scripts are performed, data is output. It is important to note that this tool does not make conclusions based on this data. This is due to the fact that the current use case of CHIMP, emotion recognition, is a placeholder and is subject to change. Changing the use case and the models used could mean different requirements for the measured KPIs.

Therefore, a few things should be considered when interpreting the data:

- The measured KPIs and their definitions are accessible through the codebase and the documentation for this project. The combinations of these KPIs per component aim to measure the most important aspects of each container. As such, the KPIs should be combined when analyzing the data for a component.  
  Example: Whilst performing a stress test on the serving API where 50,000 API requests are sent as fast as possible, the API starts returning errors after handling 13,500 requests. To identify whether this issue is hardware related, the hardware statistics can be consulted. The hardware statistics show that during the test there was a 30%/1600% CPU usage and the container used 1GB/32GB memory. This means the hardware was nowhere near its limits, and most likely not responsible for the failing of the API.

- The data is a capture of a single moment in time. For reliable results, tests should be performed regularly and with varying parameters.

- The data is heavily dependent on the hardware that is used to host the CHIMP platform. 

## Unit Tests

This project contains a number of unit tests created for the code contained within the testing tool. These unit tests were created up until October 23rd of 2025. These unit tests may not be up to date with the current code and should be updated before using them to validate the current code.

To run the tests, navigate to the folder `unit_tests_testtool` and execute the following command: `pytest unit_tests.py`.
