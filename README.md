# API Test Automation

## Overview

This project is an API test automation tool built with FastAPI. It allows you to define API test cases in JSON files, execute them, and save the results in Excel files. The tool supports both individual test execution and batch execution for multiple test files.

## Project Structure

- `main.py`: The main entry point of the FastAPI application.
- `apitest.py`: Contains the logic for loading test cases, executing them, and writing the results to Excel files.
- `requirements.txt`: Lists the dependencies required for the project.
- `results/`: Directory where the test results are saved as Excel files.
- `testfiles/`: Directory containing JSON files that define the API test cases.
- `LICENSE`: The license file for the project.
- `README.md`: This file.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns the name and version of the API.

### Run Tests

- **URL**: `/test/`
- **Method**: `POST`
- **Description**: Executes the tests defined in the specified JSON file and saves the results to an Excel file.
- **Request Body**:
    ```json
    {
        "input_file_name": "api_tests.json",
        "output_file_name": "output.xlsx",
        "environment": "dev"
    }
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "message": "Tests executed and results saved to output.xlsx"
    }
    ```

### Run All Tests

- **URL**: `/testall/`
- **Method**: `GET`
- **Description**: Executes all tests in the [testfiles](http://_vscodecontentref_/7) directory and saves the results to Excel files.
- **Optional URL Parameter**: [region](http://_vscodecontentref_/8) (e.g., `/testall/dev`)

## Defining Test Cases

Test cases are defined in JSON files located in the [testfiles](http://_vscodecontentref_/9) directory. Each test case should include the following fields:

- `name`: The name of the test case.
- [method](http://_vscodecontentref_/10): The HTTP method (e.g., GET, POST).
- [url](http://_vscodecontentref_/11): The endpoint URL.
- [headers](http://_vscodecontentref_/12): Optional HTTP headers.
- [body](http://_vscodecontentref_/13): Optional request body.
- `expected_status_code`: The expected HTTP status code.

Example:
```json
{
    "tests": [
        {
            "name": "Test GET User",
            "method": "GET",
            "url": "https://jsonplaceholder.typicode.com/users/1",
            "headers": {},
            "body": null,
            "expected_status_code": 200
        },
        {
            "name": "Test POST Create User",
            "method": "POST",
            "url": "https://jsonplaceholder.typicode.com/posts",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "title": "foo",
                "body": "bar",
                "userId": 1
            },
            "expected_status_code": 201
        }
    ]
}

License
This project is licensed under the MIT License. See the LICENSE file for details.