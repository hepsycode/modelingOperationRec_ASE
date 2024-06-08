# README Documentation for Python Project

## Overview

This document explaints how to run the IMA component, i.e., MORGAN, and replicate the experiment conducted in RQ2 and RQ3 in the paper.

## Modules Description

1. **main.py**:
   - **Purpose**: Serves as the entry point of the application, handling various operations based on user input.
   - **Functionalities**:
     - Data parsing and preprocessing for training and test datasets.
     - Execution of recommendation functions based on preprocessed data.
     - Performance evaluation across different configurations using cross-validation.
     - Interactive command-line interface for selecting operation modes.

2. **GNN_engine.py**:
   - **Purpose**: Contains the core functionalities for generating recommendations using Graph Neural Networks.
   - **Functionalities**:
     - Implementation of recommendation algorithms.
     - Evaluation of recommendation outcomes over time.

3. **dataset_utilities.py**:
   - **Purpose**: Provides utility functions for data handling and preprocessing.
   - **Functionalities**:
     - Parsing XES files for data transformation.
     - Data encoding and preprocessing for model consumption.
     - Utility functions for file and directory operations.

4. **config.py**:
   - **Purpose**: Manages configuration settings for the entire project.
   - **Functionalities**:
     - Defines paths, parameters, and other configuration settings used across modules.

## How to Run

1. Ensure Python 3.x is installed on your system.
2. Clone the repository or download the files into a local directory.
3. Navigate to the project directory in your terminal or command prompt.
4. Run the following command to start the application:
   ```bash
   python main.py
      ```   
5. Follow the on-screen prompts to select the desired operation mode.